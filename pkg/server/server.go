package server

import (
	"context"
	"encoding/json"
	"errors"
	"example/task-list/pkg/model"
	"example/task-list/pkg/service"
	"example/task-list/pkg/util"
	"log"
	"net/http"
	"strings"
	"time"
)

type ctxUserType string

const ctxUserKey ctxUserType = "userId"

type Server struct {
	Router  http.Handler
	Service *service.Service
	Config  util.Config
}

func NewServer(appService *service.Service, config util.Config) *Server {

	router := http.NewServeMux()

	appServer := &Server{
		Router:  router,
		Service: appService,
		Config:  config,
	}

	checkAccessToken := createCheckTokenMiddleware("accessToken", config.AccessTokenSecret)

	router.Handle("GET /hello", http.HandlerFunc(appServer.hello))

	router.Handle("GET /tasks", checkAccessToken(http.HandlerFunc(appServer.getTasks)))
	router.Handle("GET /tasks/{id}", checkAccessToken(http.HandlerFunc(appServer.getTask)))
	router.Handle("POST /tasks", checkAccessToken(http.HandlerFunc(appServer.postTask)))
	router.Handle("PUT /tasks/{id}", checkAccessToken(http.HandlerFunc(appServer.putTask)))
	router.Handle("DELETE /tasks/{id}", checkAccessToken(http.HandlerFunc(appServer.deleteTask)))
	router.Handle("POST /tasks/attach", checkAccessToken(http.HandlerFunc(appServer.postLabelsToTask)))
	router.Handle("POST /tasks/detach", checkAccessToken(http.HandlerFunc(appServer.deleteLabelsFromTask)))

	router.Handle("GET /labels", checkAccessToken(http.HandlerFunc(appServer.getLabels)))
	router.Handle("GET /labels/{id}", checkAccessToken(http.HandlerFunc(appServer.getLabel)))
	router.Handle("POST /labels", checkAccessToken(http.HandlerFunc(appServer.postLabel)))
	router.Handle("PUT /labels/{id}", checkAccessToken(http.HandlerFunc(appServer.putLabel)))
	router.Handle("DELETE /labels/{id}", checkAccessToken(http.HandlerFunc(appServer.deleteLabel)))

	router.Handle("POST /users/register", http.HandlerFunc(appServer.postUser))
	router.Handle("POST /users/login", http.HandlerFunc(appServer.loginUser))
	router.Handle("POST /users/logout", http.HandlerFunc(appServer.logoutUser))
	router.Handle("POST /users/token", http.HandlerFunc(appServer.createAccessToken))
	return appServer
}

// Helper functions and middleware

func httpError(w http.ResponseWriter, err error, code int) {
	errMessage := err.Error()
	message := strings.ToUpper(errMessage[:1]) + errMessage[1:]
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(model.NewMsg(message))
}

func getCookie(r *http.Request, cookieHeader string) string {
	cookie, err := r.Cookie(cookieHeader)
	if err != nil {
		log.Printf("failed to parse cookie '%v': %v", cookieHeader, err)
		return ""
	}
	return cookie.Value
}

func createCheckTokenMiddleware(cookieHeader, tokenSecret string) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			cookieValue := getCookie(r, cookieHeader)
			if cookieValue == "" {
				httpError(w, service.ErrUnauthorized, http.StatusUnauthorized)
				return
			}

			user, _, err := service.ParseToken(cookieValue, tokenSecret)
			if err != nil {
				log.Printf("failed to retrieve user from token: %v", err)
				httpError(w, service.ErrUnauthorized, http.StatusUnauthorized)
				return
			}

			ctxWithUser := context.WithValue(r.Context(), ctxUserKey, user)
			requestWithUser := r.WithContext(ctxWithUser)
			next.ServeHTTP(w, requestWithUser)
		})
	}
}

func getUserIdFromContext(r *http.Request) string {
	return r.Context().Value(ctxUserKey).(string)
}

func decodeAndValidate[T any](w http.ResponseWriter, r *http.Request) (T, error) {
	var obj T
	json.NewDecoder(r.Body).Decode(&obj)
	if err := model.Validate(obj); err != nil {
		log.Printf("validation failed: %v", err)
		httpError(w, err, http.StatusBadRequest)
		return obj, err
	}
	return obj, nil
}

func encode[T any](w http.ResponseWriter, obj T) {
	w.Header().Add("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(obj)
	if err != nil {
		log.Printf("failed to encode response: %v", err)
		httpError(w, errors.New("failed to generate response"), http.StatusInternalServerError)
	}
}

// HTTP handlers

func (s *Server) hello(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(model.NewMsg("Hello World!"))
}

func (s *Server) getTasks(w http.ResponseWriter, r *http.Request) {
	userId := getUserIdFromContext(r)

	tasks, err := s.Service.ListTasks(userId)
	if err != nil {
		httpError(w, service.ErrGetTaskFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.TaskListResponse{Tasks: tasks})
}

func (s *Server) getTask(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	userId := getUserIdFromContext(r)

	task, err := s.Service.GetTask(userId, id)
	if err == service.ErrTaskNotFound {
		httpError(w, err, http.StatusNotFound)
		return
	} else if err != nil {
		httpError(w, service.ErrListTasksFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.TaskResponse{Task: task})
}

func (s *Server) postTask(w http.ResponseWriter, r *http.Request) {
	taskReq, err := decodeAndValidate[model.TaskRequest](w, r)
	if err != nil {
		return
	}

	userId := getUserIdFromContext(r)

	task, err := s.Service.CreateTask(userId, taskReq)
	if err != nil {
		httpError(w, service.ErrCreateTaskFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.TaskResponse{Task: task})
}

func (s *Server) putTask(w http.ResponseWriter, r *http.Request) {
	taskReq, err := decodeAndValidate[model.TaskRequest](w, r)
	if err != nil {
		return
	}

	taskId := r.PathValue("id")
	userId := getUserIdFromContext(r)

	task, err := s.Service.UpdateTask(userId, taskId, taskReq)
	if err == service.ErrTaskNotFound {
		httpError(w, err, http.StatusNotFound)
		return
	} else if err != nil {
		httpError(w, service.ErrUpdateTaskFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.TaskResponse{Task: task})
}

func (s *Server) deleteTask(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	userId := getUserIdFromContext(r)

	err := s.Service.DeleteTask(userId, id)
	if err != nil {
		httpError(w, service.ErrDeleteTaskFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.NewMsg("Task deleted"))
}

func (s *Server) postLabelsToTask(w http.ResponseWriter, r *http.Request) {
	taskLabelIdsReq, err := decodeAndValidate[model.TaskLabelIdsRequest](w, r)
	if err != nil {
		return
	}
	userId := getUserIdFromContext(r)

	err = s.Service.AttachLabelsToTask(userId, taskLabelIdsReq)
	if err != nil {
		httpError(w, err, http.StatusInternalServerError)
		return
	}
	encode(w, model.NewMsg("Attached labels to task"))
}

func (s *Server) deleteLabelsFromTask(w http.ResponseWriter, r *http.Request) {
	taskLabelIdsReq, err := decodeAndValidate[model.TaskLabelIdsRequest](w, r)
	if err != nil {
		return
	}
	userId := getUserIdFromContext(r)

	err = s.Service.DetachLabelsFromTask(userId, taskLabelIdsReq)
	if err != nil {
		httpError(w, err, http.StatusInternalServerError)
		return
	}
	encode(w, model.NewMsg("Detached labels from task"))
}

func (s *Server) getLabels(w http.ResponseWriter, r *http.Request) {
	userId := getUserIdFromContext(r)

	labels, err := s.Service.ListLabels(userId)
	if err != nil {
		httpError(w, err, http.StatusInternalServerError)
		return
	}
	encode(w, model.LabelListResponse{Labels: labels})
}

func (s *Server) getLabel(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	userId := getUserIdFromContext(r)

	label, err := s.Service.GetLabel(userId, id)
	if err == service.ErrTaskNotFound {
		httpError(w, err, http.StatusNotFound)
		return
	} else if err != nil {
		httpError(w, err, http.StatusInternalServerError)
		return
	}
	encode(w, model.LabelResponse{Label: label})
}

func (s *Server) postLabel(w http.ResponseWriter, r *http.Request) {
	labelReq, err := decodeAndValidate[model.LabelRequest](w, r)
	if err != nil {
		return
	}
	userId := getUserIdFromContext(r)

	label, err := s.Service.CreateLabel(userId, labelReq)
	if err != nil {
		httpError(w, err, http.StatusInternalServerError)
		return
	}
	encode(w, model.LabelResponse{Label: label})
}

func (s *Server) putLabel(w http.ResponseWriter, r *http.Request) {
	labelReq, err := decodeAndValidate[model.LabelRequest](w, r)
	if err != nil {
		return
	}
	labelId := r.PathValue("id")
	userId := getUserIdFromContext(r)

	label, err := s.Service.UpdateLabel(userId, labelId, labelReq)
	if err == service.ErrLabelNotFound {
		httpError(w, err, http.StatusNotFound)
		return
	} else if err != nil {
		httpError(w, service.ErrUpdateLabelFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(model.LabelResponse{Label: label})
}

func (s *Server) deleteLabel(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	userId := getUserIdFromContext(r)

	err := s.Service.DeleteLabel(userId, id)
	if err != nil {
		httpError(w, service.ErrDeleteLabelFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(model.NewMsg("Label deleted"))
}

func (s *Server) postUser(w http.ResponseWriter, r *http.Request) {
	userReq, err := decodeAndValidate[model.UserRequest](w, r)
	if err != nil {
		return
	}

	user, err := s.Service.RegisterUser(userReq)
	if err == service.ErrUserExists {
		httpError(w, err, http.StatusBadRequest)
		return
	} else if err != nil {
		httpError(w, service.ErrCreateUserFailed, http.StatusInternalServerError)
		return
	}
	encode(w, model.UserResponse{User: user})
}

func (s *Server) loginUser(w http.ResponseWriter, r *http.Request) {
	userReq, err := decodeAndValidate[model.UserRequest](w, r)
	if err != nil {
		return
	}

	accessToken, refreshToken, err := s.Service.LoginUser(userReq)
	if err == service.ErrInvalidCredentials {
		httpError(w, err, http.StatusUnauthorized)
		return
	} else if err != nil {
		httpError(w, service.ErrLoginFailed, http.StatusInternalServerError)
		return
	}

	accessTokenCookie := &http.Cookie{
		Name:     "accessToken",
		Value:    accessToken,
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteDefaultMode,
		Expires:  time.Now().Add(s.Config.AccessTokenExpiry),
	}

	refreshTokenCookie := &http.Cookie{
		Name:     "refreshToken",
		Value:    refreshToken,
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteDefaultMode,
		Expires:  time.Now().Add(s.Config.RefreshTokenExpiry),
	}

	http.SetCookie(w, accessTokenCookie)
	http.SetCookie(w, refreshTokenCookie)

	encode(w, model.NewMsg("Login successful"))
}

func (s *Server) logoutUser(w http.ResponseWriter, r *http.Request) {

	accessCookieValue := getCookie(r, "accessToken")
	refreshCookieValue := getCookie(r, "refreshToken")

	s.Service.LogoutUser(accessCookieValue, refreshCookieValue)

	clearedAccessTokenCookie := &http.Cookie{
		Name:     "accessToken",
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteDefaultMode,
		MaxAge:   -1,
	}

	clearedRefreshTokenCookie := &http.Cookie{
		Name:     "refreshToken",
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteDefaultMode,
		MaxAge:   -1,
	}

	http.SetCookie(w, clearedAccessTokenCookie)
	http.SetCookie(w, clearedRefreshTokenCookie)

	encode(w, model.NewMsg("Logout successful"))
}

func (s *Server) createAccessToken(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("refreshToken")
	if err != nil {
		log.Printf("failed to parse cookie: %v", err)
		httpError(w, service.ErrUnauthorized, http.StatusUnauthorized)
		return
	}

	newAccessToken, err := s.Service.GetNewToken(cookie.Value)
	if err != nil {
		log.Printf("failed to generate new access token: %v", err)
		httpError(w, service.ErrUnauthorized, http.StatusUnauthorized)
		return
	}

	accessTokenCookie := &http.Cookie{
		Name:     "accessToken",
		Value:    newAccessToken,
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteDefaultMode,
		Expires:  time.Now().Add(time.Minute * 10),
	}

	http.SetCookie(w, accessTokenCookie)

	encode(w, model.NewMsg("Credentials refreshed"))
}
