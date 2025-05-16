package server_integration_test

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"reflect"
	"strings"
	"testing"

	"example/task-list/pkg/model"
	"example/task-list/pkg/server"
	"example/task-list/pkg/service"
	"example/task-list/pkg/store"
	"example/task-list/pkg/util"
)

// Helper functions for test cases

var testUser = model.UserRequest{Email: "foo@example.com", Password: "test"}

func marshal(t *testing.T, v any) string {
	payload, err := json.Marshal(v)
	if err != nil {
		t.Fatalf("Failed to marshal request: %v", err)
	}
	return string(payload)
}

func unmarshal[T any](t *testing.T, r io.Reader) T {
	var response T
	err := json.NewDecoder(r).Decode(&response)
	if err != nil {
		t.Logf("%v", response)
		t.Fatalf("Failed to unmarshal response: %v", err)
	}
	return response
}

// creates a test object in the database
func createTestObject[T, K any](t *testing.T, appServer *server.Server, cookies []*http.Cookie, url string, v T) K {
	payload := strings.NewReader(marshal(t, v))
	w := serveAuthRequest(appServer, cookies, http.MethodPost, url, payload)
	return unmarshal[K](t, w.Body)
}

// creates a test user and logs in as user
func createAndLoginTestUser(t *testing.T, appServer *server.Server) []*http.Cookie {
	payload := marshal(t, testUser)
	r := httptest.NewRequest(http.MethodPost, "/users/register", strings.NewReader(payload))
	w := httptest.NewRecorder()
	appServer.Router.ServeHTTP(w, r)

	r = httptest.NewRequest(http.MethodPost, "/users/login", strings.NewReader(payload))
	w = httptest.NewRecorder()
	appServer.Router.ServeHTTP(w, r)

	return w.Result().Cookies()
}

func serveAuthRequest(appServer *server.Server, cookies []*http.Cookie, method, target string, body io.Reader) *httptest.ResponseRecorder {
	r := httptest.NewRequest(method, target, body)

	for _, value := range cookies {
		r.AddCookie(value)
	}
	w := httptest.NewRecorder()
	appServer.Router.ServeHTTP(w, r)

	return w
}

func getCookies(w *httptest.ResponseRecorder) map[string]*http.Cookie {
	cookies := make(map[string]*http.Cookie)
	for _, cookie := range w.Result().Cookies() {
		cookies[cookie.Name] = cookie
	}
	return cookies
}

// cleans database, intended to be used before each test to ensure a clean state
func cleanDatabase(t *testing.T, config util.Config) {
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		config.DbUser,
		config.DbPassword,
		config.DbHost,
		config.DbPort,
		config.DbName,
	)
	db, err := sql.Open("pgx", connStr)

	if err != nil {
		t.Fatalf("unable to connect to database: %v\n", err)
	}

	_, err = db.Exec("TRUNCATE tasks, users, labels, refreshtokens, tasks_labels_map")

	if err != nil {
		t.Fatalf("unable to delete data: %v\n", err)
	}
}

// assertion functions
func assertEqual[T comparable](t *testing.T, got T, want T) {
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v to be equal to %v", got, want)
	}
}

func assertNotEqual[T comparable](t *testing.T, got T, want T) {
	if reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v to not be equal to %v", got, want)
	}
}

func assertMessageExists(t *testing.T, got util.Message) {
	if got.Message == "" {
		t.Errorf("Expected message to be set")
	}
}

func TestUserEndpoints(t *testing.T) {
	config := util.NewConfig()
	appStore := store.NewDatabaseStore(config)
	appService := service.NewService(appStore, config)
	appServer := server.NewServer(appService, config)

	t.Run("User can be registered and logged in", func(t *testing.T) {
		cleanDatabase(t, config)
		payload := marshal(t, testUser)
		r := httptest.NewRequest(http.MethodPost, "/users/register", strings.NewReader(payload))
		w := httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
		response := unmarshal[model.UserResponse](t, w.Body)

		assertEqual(t, response.User.Email, testUser.Email)

		r = httptest.NewRequest(http.MethodPost, "/users/login", strings.NewReader(payload))
		w = httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
	})

	t.Run("User token can be refreshed", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/users/token", nil)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		cookies := getCookies(w)
		if _, ok := cookies["accessToken"]; !ok {
			t.Errorf("Expected access token to be set")
		}
	})

	t.Run("User can be logged out", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/users/logout", nil)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		cookies := getCookies(w)

		assertCookieCleared := func(t *testing.T, cookie *http.Cookie, name string) {
			if cookie == nil {
				t.Errorf("Expected %s cookie to be set", name)
			} else if cookie.Value != "" {
				t.Errorf("Expected %s cookie to be empty", name)
			}
		}

		assertCookieCleared(t, cookies["accessToken"], "accessToken")
		assertCookieCleared(t, cookies["refreshToken"], "refreshToken")
	})
}

func TestLabelEndpoints(t *testing.T) {
	config := util.NewConfig()
	appStore := store.NewDatabaseStore(config)
	appService := service.NewService(appStore, config)
	appServer := server.NewServer(appService, config)
	testLabel := model.LabelRequest{Name: "test", Colour: "#ffffff"}

	t.Run("Label can be created", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)

		payload := marshal(t, testLabel)
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/labels", strings.NewReader(payload))

		response := unmarshal[model.LabelResponse](t, w.Body)

		assertEqual(t, response.Label.Name, testLabel.Name)
	})

	t.Run("All labels can be retrieved", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)

		w := serveAuthRequest(appServer, auth, http.MethodGet, "/labels", nil)
		response := unmarshal[model.LabelListResponse](t, w.Body)

		assertEqual(t, len(response.Labels), 1)
		assertEqual(t, response.Labels[0].Name, testLabel.Name)

	})

	t.Run("Can retrieve specific label", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testLabelResponse := createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)

		reqPath := fmt.Sprintf("/labels/%s", testLabelResponse.Label.Id)
		w := serveAuthRequest(appServer, auth, http.MethodGet, reqPath, nil)
		response := unmarshal[model.LabelResponse](t, w.Body)

		assertEqual(t, response.Label.Name, testLabel.Name)
	})

	t.Run("Label can be updated", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testLabelResponse := createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)

		updatedLabel := model.LabelRequest{Name: "updated", Colour: "#000000"}
		body := strings.NewReader(marshal(t, updatedLabel))
		reqPath := fmt.Sprintf("/labels/%s", testLabelResponse.Label.Id)
		w := serveAuthRequest(appServer, auth, http.MethodPut, reqPath, body)
		response := unmarshal[model.LabelResponse](t, w.Body)

		assertNotEqual(t, response.Label.Name, testLabel.Name)
	})

	t.Run("Label can be deleted", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testLabelResponse := createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)

		reqPath := fmt.Sprintf("/labels/%s", testLabelResponse.Label.Id)
		w := serveAuthRequest(appServer, auth, http.MethodDelete, reqPath, nil)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		w = serveAuthRequest(appServer, auth, http.MethodGet, reqPath, nil)
		response = unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)
	})
}

func TestTaskEndpoints(t *testing.T) {
	config := util.NewConfig()
	appStore := store.NewDatabaseStore(config)
	appService := service.NewService(appStore, config)
	appServer := server.NewServer(appService, config)
	testLabel := model.LabelRequest{Name: "test1", Colour: "#ffffff"}
	testTask := model.TaskRequest{Name: "test-task", Description: "task for testing"}

	t.Run("Task can be created", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)

		payload := marshal(t, testTask)
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/tasks", strings.NewReader(payload))
		response := unmarshal[model.TaskResponse](t, w.Body)
		t.Logf("%v", w.Body.String())

		assertEqual(t, response.Task.Name, testTask.Name)
	})

	t.Run("All tasks can be retrieved", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		createTestObject[model.TaskRequest, model.TaskResponse](t, appServer, auth, "/tasks", testTask)

		w := serveAuthRequest(appServer, auth, http.MethodGet, "/tasks", nil)
		response := unmarshal[model.TaskListResponse](t, w.Body)

		assertEqual(t, len(response.Tasks), 1)
		assertEqual(t, response.Tasks[0].Name, testTask.Name)
	})

	t.Run("Can attach label to task", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testTaskResponse := createTestObject[model.TaskRequest, model.TaskResponse](t, appServer, auth, "/tasks", testTask)
		testLabelResponse := createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)

		payload := marshal(t, model.TaskLabelIdsRequest{TaskId: testTaskResponse.Task.Id, LabelIds: []string{testLabelResponse.Label.Id}})
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/tasks/attach", strings.NewReader(payload))
		response := unmarshal[util.Message](t, w.Body)
		assertMessageExists(t, response)

		reqPath := fmt.Sprintf("/tasks/%s", testTaskResponse.Task.Id)
		w = serveAuthRequest(appServer, auth, http.MethodGet, reqPath, nil)
		taskResponse := unmarshal[model.TaskResponse](t, w.Body)

		assertEqual(t, taskResponse.Task.Name, testTask.Name)
		assertEqual(t, taskResponse.Task.Labels[0].Name, testLabel.Name)
	})

	t.Run("Can detach label from task", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testTaskResponse := createTestObject[model.TaskRequest, model.TaskResponse](t, appServer, auth, "/tasks", testTask)
		testLabelResponse := createTestObject[model.LabelRequest, model.LabelResponse](t, appServer, auth, "/labels", testLabel)
		taskAttachObj := model.TaskLabelIdsRequest{TaskId: testTaskResponse.Task.Id, LabelIds: []string{testLabelResponse.Label.Id}}
		createTestObject[model.TaskLabelIdsRequest, util.Message](t, appServer, auth, "/tasks/attach", taskAttachObj)

		payload := marshal(t, taskAttachObj)
		w := serveAuthRequest(appServer, auth, http.MethodPost, "/tasks/detach", strings.NewReader(payload))
		response := unmarshal[util.Message](t, w.Body)
		assertMessageExists(t, response)

		reqPath := fmt.Sprintf("/tasks/%s", testTaskResponse.Task.Id)
		w = serveAuthRequest(appServer, auth, http.MethodGet, reqPath, nil)
		taskResponse := unmarshal[model.TaskResponse](t, w.Body)

		assertEqual(t, taskResponse.Task.Name, testTask.Name)
		assertEqual(t, len(taskResponse.Task.Labels), 0)
	})

	t.Run("Task can be updated", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testTaskResponse := createTestObject[model.TaskRequest, model.TaskResponse](t, appServer, auth, "/tasks", testTask)

		updatedTask := model.TaskRequest{Name: "test-task-updated", Description: "task for testing"}
		body := strings.NewReader(marshal(t, updatedTask))
		reqPath := fmt.Sprintf("/tasks/%s", testTaskResponse.Task.Id)
		w := serveAuthRequest(appServer, auth, http.MethodPut, reqPath, body)
		response := unmarshal[model.TaskResponse](t, w.Body)

		assertNotEqual(t, response.Task.Name, testTask.Name)
	})

	t.Run("Task can be deleted", func(t *testing.T) {
		cleanDatabase(t, config)
		auth := createAndLoginTestUser(t, appServer)
		testTaskResponse := createTestObject[model.TaskRequest, model.TaskResponse](t, appServer, auth, "/tasks", testTask)

		reqPath := fmt.Sprintf("/tasks/%s", testTaskResponse.Task.Id)
		w := serveAuthRequest(appServer, auth, http.MethodDelete, reqPath, nil)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		w = serveAuthRequest(appServer, auth, http.MethodGet, reqPath, nil)
		response = unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)
	})
}
