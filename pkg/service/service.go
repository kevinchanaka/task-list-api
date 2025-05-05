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
	ErrTaskNotFound     = errors.New("task not found")
	ErrListTasksFailed  = errors.New("unable to retrieve tasks")
	ErrGetTaskFailed    = errors.New("unable to retrieve task")
	ErrCreateTaskFailed = errors.New("unable to create task")
	ErrUpdateTaskFailed = errors.New("unable to update task")
	ErrDeleteTaskFailed = errors.New("unable to delete task")

	ErrLabelNotFound     = errors.New("label not found")
	ErrUpdateLabelFailed = errors.New("unable to update label")
	ErrDeleteLabelFailed = errors.New("unable to delete label")

	ErrLoginFailed        = errors.New("unable to login")
	ErrUserExists         = errors.New("email address already in-use")
	ErrCreateUserFailed   = errors.New("unable to register user")
	ErrInvalidCredentials = errors.New("invalid username or password")
	ErrUnauthorized       = errors.New("unable to verify user identity")

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
		return nil, ErrListTasksFailed
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

	if err == ErrTaskNotFound {
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
		return task, ErrTaskNotFound
	}
	return task, nil
}

func (s *Service) DeleteTask(userId, taskId string) error {
	return s.Store.DeleteTask(userId, taskId)
}

func (s *Service) AttachLabelsToTask(userId string, taskLabelIdsReq model.TaskLabelIds) error {
	// TODO: check if task and labels exist (can do in DB layer)
	return s.Store.AttachLabelsToTask(userId, taskLabelIdsReq.TaskId, taskLabelIdsReq.LabelIds)
}

func (s *Service) DetachLabelsFromTask(userId string, taskLabelIdsReq model.TaskLabelIds) error {
	// TODO: check if task and labels exist (can do in DB layer)
	return s.Store.DetachLabelsFromTask(userId, taskLabelIdsReq.TaskId, taskLabelIdsReq.LabelIds)
}

func (s *Service) ListLabels(userId string) ([]model.Label, error) {
	labels, err := s.Store.ListLabels(userId)
	if err != nil {
		return nil, err
	}
	return labels, err
}

func (s *Service) CreateLabel(userId string, labelReq model.LabelRequest) (model.Label, error) {
	label := model.NewLabel(userId, labelReq.Name, labelReq.Colour)
	if err := s.Store.CreateLabel(label); err != nil {
		return label, err
	}
	return label, nil
}

func (s *Service) GetLabel(userId, labelId string) (model.Label, error) {
	label, err := s.Store.GetLabel(userId, labelId)
	if err == store.ErrRecordNotFound {
		return label, ErrLabelNotFound
	}
	return label, nil
}

func (s *Service) UpdateLabel(userId string, labelId string, labelReq model.LabelRequest) (model.Label, error) {

	label, err := s.GetLabel(userId, labelId)

	if err == ErrLabelNotFound {
		return model.Label{}, err
	}

	label.Name = labelReq.Name
	label.Colour = labelReq.Colour
	label.UpdatedAt = time.Now().UTC().Format(time.RFC3339)

	if err := s.Store.UpdateLabel(label); err != nil {
		return model.Label{}, err
	}
	return label, nil
}

func (s *Service) DeleteLabel(userId, labelId string) error {
	return s.Store.DeleteLabel(userId, labelId)
}

func (s *Service) RegisterUser(userReq util.UserRequest) (model.User, error) {

	_, err := s.Store.GetUser(userReq.Email)
	if err == nil {
		return model.User{}, ErrUserExists
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
		return "", "", ErrInvalidCredentials
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(userReq.Password))
	if err != nil {
		return "", "", ErrInvalidCredentials
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
	_, accessTokenParsed, _ := ParseToken(accessToken, s.Config.AccessTokenSecret)
	_, refreshTokenParsed, _ := ParseToken(refreshToken, s.Config.RefreshTokenSecret)

	s.Store.DeleteToken(accessTokenParsed)
	s.Store.DeleteToken(refreshTokenParsed)
}

func (s *Service) GetNewToken(refreshToken string) (string, error) {

	_, refreshTokenParsed, err := ParseToken(refreshToken, s.Config.RefreshTokenSecret)
	if err != nil {
		log.Printf("failed to parse refresh token: %v", err)
		return "", err
	}

	// NOTE: this is performed to handle logout scenarios (refresh token is deleted from db)
	token, err := s.Store.GetToken(refreshTokenParsed)
	if err != nil {
		log.Printf("unable to find token in database: %v", err)
		return "", err
	}

	accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": token.UserId,
		"exp": time.Now().Add(time.Minute * 10).Unix(),
	})
	signedAccessToken, err := accessToken.SignedString([]byte(s.Config.AccessTokenSecret))
	if err != nil {
		log.Printf("failed to generate access token: %v", err)
		return "", err
	}

	return signedAccessToken, nil
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
