package server_integration_test

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"example/task-list/pkg/model"
	"example/task-list/pkg/server"
	"example/task-list/pkg/service"
	"example/task-list/pkg/store"
	"example/task-list/pkg/util"
)

// Helper functions for test cases

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
		t.Fatalf("Failed to unmarshal response: %v", err)
	}
	return response
}

// creates a new user, logs in and issues HTTP request as that user
func newAuthenticatedRequest(t *testing.T, appServer *server.Server, method, target string, body io.Reader) *http.Request {
	user := model.UserRequest{Email: "foo@example.com", Password: "test"}
	payload := marshal(t, user)
	r := httptest.NewRequest(http.MethodPost, "/users/register", strings.NewReader(payload))
	w := httptest.NewRecorder()
	appServer.Router.ServeHTTP(w, r)

	r = httptest.NewRequest(http.MethodPost, "/users/login", strings.NewReader(payload))
	w = httptest.NewRecorder()
	appServer.Router.ServeHTTP(w, r)

	r = httptest.NewRequest(method, target, body)
	cookies := w.Result().Cookies()

	for _, value := range cookies {
		r.AddCookie(value)
	}

	return r
}

func getCookies(t *testing.T, w *httptest.ResponseRecorder) map[string]*http.Cookie {
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
		testUser := model.UserRequest{Email: "foo@example.com", Password: "test"}
		payload := marshal(t, testUser)
		r := httptest.NewRequest(http.MethodPost, "/users/register", strings.NewReader(payload))
		w := httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
		response := unmarshal[model.UserResponse](t, w.Body)

		got := response.User.Email
		want := testUser.Email
		if got != want {
			t.Errorf("Expected %v to be equal to %v", got, want)
		}

		r = httptest.NewRequest(http.MethodPost, "/users/login", strings.NewReader(payload))
		w = httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
	})

	t.Run("User token can be refreshed", func(t *testing.T) {
		cleanDatabase(t, config)
		r := newAuthenticatedRequest(t, appServer, http.MethodPost, "/users/token", nil)
		w := httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		cookies := getCookies(t, w)
		if _, ok := cookies["accessToken"]; !ok {
			t.Errorf("Expected access token to be set")
		}
	})

	t.Run("User can be logged out", func(t *testing.T) {
		cleanDatabase(t, config)
		r := newAuthenticatedRequest(t, appServer, http.MethodPost, "/users/logout", nil)
		w := httptest.NewRecorder()
		appServer.Router.ServeHTTP(w, r)
		response := unmarshal[util.Message](t, w.Body)

		assertMessageExists(t, response)

		cookies := getCookies(t, w)

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

	cleanDatabase(t, config)
}

// TODO: test the following in order:
// label endpoints
// task endpoints (including attaching labels)
