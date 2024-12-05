package database

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func DBinstance() *mongo.Client {
	err := godotenv.Load(".env")
	if err!= nil {
		log.Fatal("Error loading env file")
	}

	MongoDb := os.Getenv("MONGODB_URI")

	client, err := mongo.NewClient(options.Client().ApplyURI(MongoDb))

	if err != nil {
		log.Fatal(err)
	}

	ctx, cancel :=  context.WithTimeout(context.Background(), 10*time.Second)

	defer cancel()

	err = client.Connect(ctx)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB")

	return client

}
var Client *mongo.Client = DBinstance()

func OpenCollection(client *mongo.Client, colectionName string) *mongo.Collection {
	var colection *mongo.Collection = client.Database("MyDatabase").Collection(colectionName)
	return colection
}