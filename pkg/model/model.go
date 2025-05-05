package model

import (
	"log"
	"time"

	"github.com/google/uuid"

	"golang.org/x/crypto/bcrypt"
)

type Task struct {
	Id          string      `json:"id"`
	UserId      string      `json:"userId"`
	Name        string      `json:"name"`
	Description string      `json:"description"`
	Completed   bool        `json:"completed"`
	CreatedAt   string      `json:"createdAt"`
	UpdatedAt   string      `json:"updatedAt"`
	Labels      []TaskLabel `json:"labels"`
}

type TaskLabel struct {
	Id     string `json:"id"`
	Name   string `json:"name"`
	Colour string `json:"colour"`
}

type Label struct {
	Id        string `json:"id"`
	UserId    string `json:"userId"`
	Name      string `json:"name"`
	Colour    string `json:"colour"`
	CreatedAt string `json:"createdAt"`
	UpdatedAt string `json:"updatedAt"`
}

type LabelRequest struct {
	Name   string `json:"name"`
	Colour string `json:"colour"`
}

type LabelListResponse struct {
	Labels []Label `json:"labels"`
}

type LabelResponse struct {
	Label Label `json:"label"`
}

type TaskLabelIds struct {
	TaskId   string   `json:"taskId"`
	LabelIds []string `json:"labelIds"`
}

type User struct {
	Id           string `json:"id"`
	Email        string `json:"email"`
	PasswordHash string `json:"-"`
}

type Token struct {
	Token  string
	UserId string
	Expiry int64
}

func NewTask(userId, name, description string) Task {
	creationTime := time.Now().UTC().Format(time.RFC3339)
	return Task{
		Id:          uuid.New().String(),
		Name:        name,
		Description: description,
		UserId:      userId,
		Completed:   false,
		CreatedAt:   creationTime,
		UpdatedAt:   creationTime,
	}
}

func NewLabel(userId, name, colour string) Label {
	creationTime := time.Now().UTC().Format(time.RFC3339)
	return Label{
		Id:        uuid.New().String(),
		Name:      name,
		Colour:    colour,
		CreatedAt: creationTime,
		UpdatedAt: creationTime,
		UserId:    userId,
	}
}

func NewUser(email, password string) (User, error) {
	passwordHash, err := bcrypt.GenerateFromPassword([]byte(password), 0)
	if err != nil {
		log.Printf("error while generating password hash: %v", err)
		return User{}, err
	}
	return User{
		Id:           uuid.New().String(),
		Email:        email,
		PasswordHash: string(passwordHash),
	}, nil
}

func NewToken(token, userId string, expiry int64) Token {
	return Token{
		Token:  token,
		UserId: userId,
		Expiry: expiry,
	}
}
