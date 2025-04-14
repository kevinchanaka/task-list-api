package util

import (
	"errors"
	"example/task-list/pkg/model"
)

type TaskRequest struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Completed   bool   `json:"completed"`
}

type TaskListResponse struct {
	Tasks []model.Task `json:"tasks"`
}

type TaskResponse struct {
	Task model.Task `json:"task"`
}

func ValidateTaskRequest(taskReq TaskRequest) error { // TODO: replace this with a library
	if taskReq.Name == "" {
		return errors.New("task name cannot be empty")
	}
	if taskReq.Description == "" {
		return errors.New("task description cannot be empty")
	}
	if len(taskReq.Name) > 255 {
		return errors.New("task name cannot exceed 255 characters")
	}
	if len(taskReq.Description) > 255 {
		return errors.New("task description cannot exceed 255 characters")
	}
	return nil
}

type UserRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type UserResponse struct {
	User model.User `json:"user"`
}

type LoginResponse struct {
	AccessToken  string `json:"accessToken"`
	RefreshToken string `json:"refreshToken"`
}
