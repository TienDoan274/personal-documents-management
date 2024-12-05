package models

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
	"time"
)

type User struct {
	ID primitive.ObjectID 	`bson: "_id"`
	Username *string        `json: "username",validate: "required, min=2, max = 20"`
	Email *string			`json: "email", validate: "email, required"`
	Password *string		`json: "password" ,validate: "required, min=8 "`
	Phone *string			`json: "phone" ,validate:"required"`
	Token *string			`json: "token"`
	User_type *string 		`json: "user_type", validate: "required, eq=ADMIN|eq=USER"`
	Refresh_token *string	`json: "refresh_token"`
	Created_date time.Time	`json: "created_date"`
	Updated_date time.Time	`json: "updated_date"`
	User_id	string			`json: "user_id"`
}

