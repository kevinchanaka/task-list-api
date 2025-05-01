package server

import (
	"context"
	"encoding/json"
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

	router.Handle("GET /hello", jsonHeader(http.HandlerFunc(appServer.hello)))
	router.Handle("GET /tasks", jsonHeader(checkAccessToken(http.HandlerFunc(appServer.getTasks))))
	router.Handle("GET /tasks/{id}", jsonHeader(checkAccessToken(http.HandlerFunc(appServer.getTask))))
	router.Handle("POST /tasks", jsonHeader(checkAccessToken(http.HandlerFunc(appServer.postTask))))
	router.Handle("PUT /tasks/{id}", jsonHeader(checkAccessToken(http.HandlerFunc(appServer.putTask))))
	router.Handle("DELETE /tasks/{id}", jsonHeader(checkAccessToken(http.HandlerFunc(appServer.deleteTask))))

	router.Handle("POST /users/register", jsonHeader(http.HandlerFunc(appServer.postUser)))
	router.Handle("POST /users/login", jsonHeader(http.HandlerFunc(appServer.loginUser)))
	router.Handle("POST /users/logout", jsonHeader(http.HandlerFunc(appServer.logoutUser)))
	router.Handle("POST /users/token", jsonHeader(http.HandlerFunc(appServer.createAccessToken)))
	return appServer
}

// Helper functions and middleware

func httpError(w http.ResponseWriter, err error, code int) {
	errMessage := err.Error()
	message := strings.ToUpper(errMessage[:1]) + errMessage[1:]
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(util.NewMsg(message))
}

func jsonHeader(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	})
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

// HTTP handlers

func (s *Server) hello(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(util.NewMsg("Hello World!"))
}

func (s *Server) getTasks(w http.ResponseWriter, r *http.Request) {
	userId := getUserIdFromContext(r)

	tasks, err := s.Service.ListTasks(userId)
	if err != nil {
		httpError(w, service.ErrGetTaskFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(util.TaskListResponse{Tasks: tasks})
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
	json.NewEncoder(w).Encode(util.TaskResponse{Task: task})
}

func (s *Server) postTask(w http.ResponseWriter, r *http.Request) {
	var taskReq util.TaskRequest
	json.NewDecoder(r.Body).Decode(&taskReq)
	if err := util.ValidateTaskRequest(taskReq); err != nil {
		httpError(w, err, http.StatusBadRequest)
		return
	}

	userId := getUserIdFromContext(r)

	task, err := s.Service.CreateTask(userId, taskReq)
	if err != nil {
		httpError(w, service.ErrCreateTaskFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(util.TaskResponse{Task: task})
}

func (s *Server) putTask(w http.ResponseWriter, r *http.Request) {
	var taskReq util.TaskRequest
	json.NewDecoder(r.Body).Decode(&taskReq)
	if err := util.ValidateTaskRequest(taskReq); err != nil {
		httpError(w, err, http.StatusBadRequest)
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
	json.NewEncoder(w).Encode(util.TaskResponse{Task: task})
}

func (s *Server) deleteTask(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	userId := getUserIdFromContext(r)

	err := s.Service.DeleteTask(userId, id)
	if err != nil {
		httpError(w, service.ErrDeleteTaskFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(util.NewMsg("Task deleted"))
}

func (s *Server) postUser(w http.ResponseWriter, r *http.Request) {
	var userReq util.UserRequest
	json.NewDecoder(r.Body).Decode(&userReq) // TODO: validation

	user, err := s.Service.RegisterUser(userReq)
	if err == service.ErrUserExists {
		httpError(w, err, http.StatusBadRequest)
		return
	} else if err != nil {
		httpError(w, service.ErrCreateUserFailed, http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(util.UserResponse{User: user})
}

func (s *Server) loginUser(w http.ResponseWriter, r *http.Request) {
	var userReq util.UserRequest
	json.NewDecoder(r.Body).Decode(&userReq) // TODO: validation

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

	json.NewEncoder(w).Encode(util.NewMsg("Login successful"))
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

	json.NewEncoder(w).Encode(util.NewMsg("Logout successful"))
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

	json.NewEncoder(w).Encode(util.NewMsg("Credentials refreshed"))
}
