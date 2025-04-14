package model

import (
	"log"
	"time"

	"github.com/google/uuid"

	"golang.org/x/crypto/bcrypt"
)

type Task struct {
	Id          string `json:"id"`
	UserId      string
	Name        string `json:"name"`
	Description string `json:"description"`
	Completed   bool   `json:"completed"`
	CreatedAt   string `json:"createdAt"`
	UpdatedAt   string `json:"updatedAt"`
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
