package util

import "encoding/json"

type Message struct {
	Message string `json:"message"`
}

func NewMsg(message string) Message {
	return Message{message}
}

func NewMsgStr(message string) string {
	return Message{message}.String()
}

func (m Message) String() string {
	errBytes, _ := json.Marshal(m)
	return string(errBytes)
}
