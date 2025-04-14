package util

import "errors"

var ErrTaskNotFound = errors.New("task not found")
var ErrListTasksFailed = errors.New("unable to retrieve tasks")
var ErrGetTaskFailed = errors.New("unable to retrieve task")
var ErrCreateTaskFailed = errors.New("unable to create task")
var ErrUpdateTaskFailed = errors.New("unable to update task")
var ErrDeleteTaskFailed = errors.New("unable to delete task")

var ErrLoginFailed = errors.New("unable to login")
var ErrUserExists = errors.New("email address already in-use")
var ErrCreateUserFailed = errors.New("unable to register user")
var ErrInvalidCredentials = errors.New("invalid username or password")
var ErrParseTokenFailed = errors.New("unable to parse token")
var ErrUnauthorized = errors.New("unable to verify user identity")
