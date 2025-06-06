package store

import (
	"database/sql"
	"errors"
	"example/task-list/pkg/model"
	"example/task-list/pkg/util"
	"fmt"
	"log"
	"strconv"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
)

// Implement data store via Postgres here
// TRY not to mix with too much business logic, try to decouple as much as possible
// This lib should only need to deal with interacting with a postgres database and storing/retrieving data

var ErrRecordNotFound = errors.New("record not found")

type Store interface {
	ListTasks(string) ([]model.Task, error)
	CreateTask(model.Task) error
	UpdateTask(model.Task) error
	GetTask(string, string) (model.Task, error)
	DeleteTask(string, string) error
	AttachLabelsToTask(string, string, []string) error
	DetachLabelsFromTask(string, string, []string) error
	ListLabels(string) ([]model.Label, error)
	CreateLabel(model.Label) error
	GetLabel(string, string) (model.Label, error)
	UpdateLabel(model.Label) error
	DeleteLabel(string, string) error
	CreateUser(model.User) error
	GetUser(string) (model.User, error)
	CreateToken(model.Token) error
	GetToken(string) (model.Token, error)
	DeleteToken(string) error
}

type DatabaseStore struct {
	db *sql.DB
}

func NewDatabaseStore(config util.Config) Store {
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		config.DbUser,
		config.DbPassword,
		config.DbHost,
		config.DbPort,
		config.DbName,
	)
	db, err := sql.Open("pgx", connStr)

	if err != nil {
		log.Fatalf("unable to connect to database: %v\n", err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatalf("unable to ping database: %v\n", err)
	}

	return &DatabaseStore{db: db}
}

func isoToUnixTime(inputTime string) int64 {
	parsedTime, _ := time.Parse(time.RFC3339, inputTime)
	return parsedTime.Unix()
}

func unixToIsoTime(inputTime string) string {
	inputTimeInt, _ := strconv.ParseInt(inputTime, 10, 64)
	parsedTime := time.Unix(inputTimeInt, 0)
	return parsedTime.UTC().Format(time.RFC3339)
}

func (s *DatabaseStore) ListTasks(userId string) ([]model.Task, error) {
	rows, err := s.db.Query("SELECT * from tasks WHERE userId = $1", userId)
	if err != nil {
		log.Printf("error while running query: %v", err)
		return nil, err
	}
	defer rows.Close()

	tasks := []model.Task{}
	for rows.Next() {
		var task model.Task
		if err := rows.Scan(&task.Id, &task.Name, &task.Description, &task.Completed, &task.CreatedAt, &task.UpdatedAt, &task.UserId); err != nil {
			log.Printf("error while scanning query result: %v", err)
			return nil, err
		}
		task.CreatedAt = unixToIsoTime(task.CreatedAt)
		task.UpdatedAt = unixToIsoTime(task.UpdatedAt)

		// TODO: query for all labels in one go using IN condition or JOIN
		rows, err := s.db.Query("SELECT labelId from tasks_labels_map WHERE taskId = $1", task.Id)
		if err != nil {
			log.Printf("error while running query: %v", err)
			return nil, err
		}
		defer rows.Close()

		labels := []model.TaskLabel{}
		for rows.Next() {
			var labelId string
			if err := rows.Scan(&labelId); err != nil {
				log.Printf("error while scanning query result: %v", err)
				return nil, err
			}
			var label model.TaskLabel
			row := s.db.QueryRow("SELECT id, name, colour from labels WHERE userId = $1 AND id = $2", userId, labelId)
			if err := row.Scan(&label.Id, &label.Name, &label.Colour); err != nil {
				if err == sql.ErrNoRows {
					return nil, ErrRecordNotFound
				}
				log.Printf("unable to retrieve label: %v", err)
				return nil, err
			}
			labels = append(labels, label)
		}
		task.Labels = labels
		tasks = append(tasks, task)
	}
	if err := rows.Err(); err != nil {
		log.Printf("incomplete query result: %v", err)
		return nil, err
	}
	return tasks, nil
}

func (s *DatabaseStore) CreateTask(task model.Task) error {
	_, err := s.db.Exec("INSERT INTO tasks (id, name, description, completed, createdAt, updatedAt, userId) VALUES ($1, $2, $3, $4, $5, $6, $7)",
		task.Id, task.Name, task.Description, task.Completed, isoToUnixTime(task.CreatedAt), isoToUnixTime(task.UpdatedAt), task.UserId)
	if err != nil {
		log.Printf("failed to insert record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) UpdateTask(task model.Task) error {
	_, err := s.db.Exec("UPDATE tasks SET name = $1, description = $2, completed = $3, updatedAt = $4 WHERE userId = $5 AND id = $6",
		task.Name, task.Description, task.Completed, isoToUnixTime(task.UpdatedAt), task.UserId, task.Id)
	if err != nil {
		log.Printf("failed to update record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) GetTask(userId string, taskId string) (model.Task, error) {
	var task model.Task
	row := s.db.QueryRow("SELECT * from tasks WHERE userId = $1 AND id = $2", userId, taskId)
	if err := row.Scan(&task.Id, &task.Name, &task.Description, &task.Completed, &task.CreatedAt, &task.UpdatedAt, &task.UserId); err != nil {
		if err == sql.ErrNoRows {
			return model.Task{}, ErrRecordNotFound
		}
		log.Printf("unable to retrieve task: %v", err)
		return model.Task{}, err
	}
	task.CreatedAt = unixToIsoTime(task.CreatedAt)
	task.UpdatedAt = unixToIsoTime(task.UpdatedAt)

	rows, err := s.db.Query("SELECT labelId from tasks_labels_map WHERE taskId = $1", taskId)
	if err != nil {
		log.Printf("error while running query: %v", err)
		return model.Task{}, err
	}
	defer rows.Close()

	// TODO: query for all labels in one go using IN condition or JOIN
	labels := []model.TaskLabel{}
	for rows.Next() {
		var labelId string
		if err := rows.Scan(&labelId); err != nil {
			log.Printf("error while scanning query result: %v", err)
			return model.Task{}, err
		}
		var label model.TaskLabel
		row := s.db.QueryRow("SELECT id, name, colour from labels WHERE userId = $1 AND id = $2", userId, labelId)
		if err := row.Scan(&label.Id, &label.Name, &label.Colour); err != nil {
			if err == sql.ErrNoRows {
				return model.Task{}, ErrRecordNotFound
			}
			log.Printf("unable to retrieve label: %v", err)
			return model.Task{}, err
		}
		labels = append(labels, label)
	}
	task.Labels = labels
	return task, nil
}

func (s *DatabaseStore) DeleteTask(userId string, taskId string) error {
	_, err := s.db.Exec("DELETE FROM tasks WHERE userId = $1 AND id = $2", userId, taskId)
	if err != nil {
		log.Printf("failed to delete record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) AttachLabelsToTask(userId string, taskId string, labelIds []string) error {
	tx, err := s.db.Begin()
	if err != nil {
		log.Printf("failed to begin transaction: %v", err)
		return err
	}

	defer tx.Rollback()

	for _, labelId := range labelIds {
		_, err := tx.Exec("INSERT INTO tasks_labels_map (taskId, labelId) VALUES ($1, $2)", taskId, labelId)
		if err != nil {
			log.Printf("failed to insert record: %v", err)
			return err
		}
	}

	if err := tx.Commit(); err != nil {
		log.Printf("failed to commit transaction: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) DetachLabelsFromTask(userId string, taskId string, labelIds []string) error {
	tx, err := s.db.Begin()
	if err != nil {
		log.Printf("failed to begin transaction: %v", err)
		return err
	}

	defer tx.Rollback()

	for _, labelId := range labelIds {
		_, err := tx.Exec("DELETE FROM tasks_labels_map WHERE taskId = $1 AND labelId = $2", taskId, labelId)
		if err != nil {
			log.Printf("failed to delete record: %v", err)
			return err
		}
	}

	if err := tx.Commit(); err != nil {
		log.Printf("failed to commit transaction: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) ListLabels(userId string) ([]model.Label, error) {
	rows, err := s.db.Query("SELECT * from labels WHERE userId = $1", userId)
	if err != nil {
		log.Printf("error while running query: %v", err)
		return nil, err
	}
	defer rows.Close()
	labels := []model.Label{}
	for rows.Next() {
		var label model.Label
		if err := rows.Scan(&label.Id, &label.Name, &label.Colour, &label.CreatedAt, &label.UpdatedAt, &label.UserId); err != nil {
			log.Printf("error while scanning query result: %v", err)
			return nil, err
		}
		label.CreatedAt = unixToIsoTime(label.CreatedAt)
		label.UpdatedAt = unixToIsoTime(label.UpdatedAt)
		labels = append(labels, label)
	}
	if err := rows.Err(); err != nil {
		log.Printf("incomplete query result: %v", err)
		return nil, err
	}
	return labels, nil
}

func (s *DatabaseStore) CreateLabel(label model.Label) error {
	_, err := s.db.Exec("INSERT INTO labels (id, name, colour, createdAt, updatedAt, userId) VALUES ($1, $2, $3, $4, $5, $6)",
		label.Id, label.Name, label.Colour, isoToUnixTime(label.CreatedAt), isoToUnixTime(label.UpdatedAt), label.UserId)
	if err != nil {
		log.Printf("failed to insert record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) GetLabel(userId string, labelId string) (model.Label, error) {
	var label model.Label
	row := s.db.QueryRow("SELECT * from labels WHERE userId = $1 AND id = $2", userId, labelId)
	if err := row.Scan(&label.Id, &label.Name, &label.Colour, &label.CreatedAt, &label.UpdatedAt, &label.UserId); err != nil {
		if err == sql.ErrNoRows {
			return model.Label{}, ErrRecordNotFound
		}
		log.Printf("unable to retrieve task: %v", err)
		return model.Label{}, err
	}
	label.CreatedAt = unixToIsoTime(label.CreatedAt)
	label.UpdatedAt = unixToIsoTime(label.UpdatedAt)
	return label, nil
}

func (s *DatabaseStore) UpdateLabel(label model.Label) error {
	_, err := s.db.Exec("UPDATE labels SET name = $1, colour = $2, updatedAt = $3 WHERE userId = $4 AND id = $5",
		label.Name, label.Colour, isoToUnixTime(label.UpdatedAt), label.UserId, label.Id)
	if err != nil {
		log.Printf("failed to update record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) DeleteLabel(userId string, labelId string) error {
	_, err := s.db.Exec("DELETE FROM labels WHERE userId = $1 AND id = $2", userId, labelId)
	if err != nil {
		log.Printf("failed to delete record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) CreateUser(user model.User) error {
	_, err := s.db.Exec("INSERT INTO users (id, email, passwordHash) VALUES ($1, $2, $3)", user.Id, user.Email, user.PasswordHash)
	if err != nil {
		log.Printf("failed to insert record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) GetUser(email string) (model.User, error) {
	var user model.User
	row := s.db.QueryRow("SELECT * from users WHERE email = $1", email)
	if err := row.Scan(&user.Id, &user.Email, &user.PasswordHash); err != nil {
		if err == sql.ErrNoRows {
			return model.User{}, ErrRecordNotFound
		}
		log.Printf("unable to retrieve user: %v", err)
		return model.User{}, err
	}
	return user, nil
}

func (s *DatabaseStore) CreateToken(token model.Token) error {
	_, err := s.db.Exec("INSERT INTO refreshtokens (token, userId, expiry) VALUES ($1, $2, $3)", token.Token, token.UserId, token.Expiry)
	if err != nil {
		log.Printf("failed to insert record: %v", err)
		return err
	}
	return nil
}

func (s *DatabaseStore) GetToken(token string) (model.Token, error) {
	var tokenObj model.Token
	row := s.db.QueryRow("SELECT * from refreshtokens WHERE token = $1", token)
	if err := row.Scan(&tokenObj.Token, &tokenObj.UserId, &tokenObj.Expiry); err != nil {
		if err == sql.ErrNoRows {
			return model.Token{}, ErrRecordNotFound
		}
		log.Printf("unable to retrieve token: %v", err)
		return model.Token{}, err
	}
	return tokenObj, nil
}

func (s *DatabaseStore) DeleteToken(token string) error {
	_, err := s.db.Query("DELETE FROM refreshtokens WHERE token = $1", token)
	if err != nil {
		log.Printf("failed to delete record: %v", err)
		return err
	}
	return nil
}
