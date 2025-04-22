package service

import (
	"errors"
	"example/task-list/pkg/model"
	"example/task-list/pkg/store"
	"example/task-list/pkg/util"
	"fmt"
	"log"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

var (
	ErrParseTokenFailed      = errors.New("failed to parse token")
	ErrRetrieveSubjectFailed = errors.New("failed to retrieve subject from token")
)

type Service struct {
	Store  store.Store
	Config util.Config
}

func NewService(store store.Store, config util.Config) *Service {
	return &Service{Store: store, Config: config}
}

func (s *Service) ListTasks(userId string) ([]model.Task, error) {
	tasks, err := s.Store.ListTasks(userId)
	if err != nil {
		return nil, util.ErrListTasksFailed
	}
	return tasks, err
}

func (s *Service) CreateTask(userId string, taskReq util.TaskRequest) (model.Task, error) {
	task := model.NewTask(userId, taskReq.Name, taskReq.Description)
	if err := s.Store.CreateTask(task); err != nil {
		return task, err
	}
	return task, nil
}

func (s *Service) UpdateTask(userId string, taskId string, taskReq util.TaskRequest) (model.Task, error) {

	task, err := s.GetTask(userId, taskId)

	if err == util.ErrTaskNotFound {
		return model.Task{}, err
	}

	task.Name = taskReq.Name
	task.Description = taskReq.Description
	task.Completed = taskReq.Completed
	task.UpdatedAt = time.Now().UTC().Format(time.RFC3339)

	if err := s.Store.UpdateTask(task); err != nil {
		return model.Task{}, err
	}
	return task, nil
}

func (s *Service) GetTask(userId, taskId string) (model.Task, error) {
	task, err := s.Store.GetTask(userId, taskId)
	if err == store.ErrRecordNotFound {
		return task, util.ErrTaskNotFound
	}
	return task, nil
}

func (s *Service) DeleteTask(userId, taskId string) error {
	return s.Store.DeleteTask(userId, taskId)
}

func (s *Service) RegisterUser(userReq util.UserRequest) (model.User, error) {

	_, err := s.Store.GetUser(userReq.Email)
	if err == nil {
		return model.User{}, util.ErrUserExists
	}

	user, err := model.NewUser(userReq.Email, userReq.Password)
	if err != nil {
		return model.User{}, err
	}

	err = s.Store.CreateUser(user)
	if err != nil {
		return model.User{}, err
	}
	return user, nil
}

func (s *Service) LoginUser(userReq util.UserRequest) (string, string, error) {

	user, err := s.Store.GetUser(userReq.Email)
	if err == store.ErrRecordNotFound {
		return "", "", util.ErrInvalidCredentials
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(userReq.Password))
	if err != nil {
		return "", "", util.ErrInvalidCredentials
	}

	accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": user.Id,
		"exp": time.Now().Add(time.Minute * 10).Unix(),
	})
	refreshTokenExpiry := time.Now().Add(time.Minute * 20).Unix()
	refreshToken := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": user.Id,
		"exp": refreshTokenExpiry,
	})

	signedAccessToken, err := accessToken.SignedString([]byte(s.Config.AccessTokenSecret))
	if err != nil {
		log.Printf("failed to generate access token: %v", err)
		return "", "", err
	}

	signedRefreshToken, err := refreshToken.SignedString([]byte(s.Config.RefreshTokenSecret))
	if err != nil {
		log.Printf("failed to generate refresh token: %v", err)
		return "", "", err
	}

	refreshTokenObj := model.NewToken(signedRefreshToken, user.Id, refreshTokenExpiry)
	err = s.Store.CreateToken(refreshTokenObj)
	if err != nil {
		log.Printf("failed to store refresh token: %v", err)
		return "", "", err
	}

	return signedAccessToken, signedRefreshToken, nil

}

func (s *Service) LogoutUser(accessToken string, refreshToken string) {
	s.Store.DeleteToken(accessToken)
	s.Store.DeleteToken(refreshToken)
}

func (s *Service) GetNewToken(userId, refreshToken string) string { // TODO: make this better, don't log out user if token is invalid

	tokenValid := true

	token, err := s.Store.GetToken(refreshToken)
	if err != nil {
		log.Printf("failed to get token: %v", err)
		tokenValid = false
	}

	if token.UserId != userId {
		log.Printf("token userId %v does not match userId %v", token.UserId, userId)
		tokenValid = false
	}

	if token.Expiry < time.Now().Unix() {
		log.Printf("token has already expired")
		tokenValid = false
	}

	if !tokenValid {
		s.LogoutUser("", refreshToken)
		return ""
	}

	accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": token.UserId,
		"exp": time.Now().Add(time.Minute * 10).Unix(),
	})
	signedAccessToken, err := accessToken.SignedString([]byte(s.Config.AccessTokenSecret))
	if err != nil {
		log.Printf("failed to generate access token: %v", err)
		s.LogoutUser("", refreshToken)
		return ""
	}

	return signedAccessToken
}

func ParseToken(tokenString string, tokenSecret string) (string, string, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (any, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(tokenSecret), nil
	})

	if err != nil {
		log.Printf("failed to parse token: %v", err)
		return "", "", ErrParseTokenFailed
	}

	sub, err := token.Claims.GetSubject()
	if err != nil {
		log.Printf("failed to retrieve subject from token: %v", err)
		return "", token.Raw, ErrRetrieveSubjectFailed
	}

	return sub, token.Raw, nil
}
