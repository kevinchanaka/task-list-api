package model

import (
	"fmt"

	"github.com/go-playground/validator/v10"
)

var validate *validator.Validate = validator.New(validator.WithRequiredStructEnabled())

func Validate[T any](obj T) error {
	validationErr := validate.Struct(obj)
	if validationErr != nil {
		err := validationErr.(validator.ValidationErrors)[0]
		switch err.Tag() {
		case "required":
			return fmt.Errorf("%s is required", err.Field())
		case "max":
			return fmt.Errorf("%s exceeds max length of %s", err.Field(), err.Param())
		default:
			return fmt.Errorf("%s failed validation: %s", err.Field(), err.Tag())
		}
	}
	return nil
}

type TaskRequest struct {
	Name        string `json:"name" validate:"required"`
	Description string `json:"description" validate:"required"`
	Completed   bool   `json:"completed" validate:"required"`
}

type TaskListResponse struct {
	Tasks []Task `json:"tasks"`
}

type TaskResponse struct {
	Task Task `json:"task"`
}

type UserRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type UserResponse struct {
	User User `json:"user"`
}

type LoginResponse struct {
	AccessToken  string `json:"accessToken"`
	RefreshToken string `json:"refreshToken"`
}

type LabelRequest struct {
	Name   string `json:"name" validate:"required"`
	Colour string `json:"colour" validate:"required,hexcolor"`
}

type LabelListResponse struct {
	Labels []Label `json:"labels"`
}

type LabelResponse struct {
	Label Label `json:"label"`
}

type TaskLabelIdsRequest struct {
	TaskId   string   `json:"taskId" validate:"required"`
	LabelIds []string `json:"labelIds" validate:"required"`
}
