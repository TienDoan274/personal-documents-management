package routes

import (
	"github.com/gin-gonic/gin"
	middleware "service-user/middleware"
	controller "service-user/controllers"
)

func UserRoutes(incomingRouter *gin.Engine) {
	incomingRouter.Use(middleware.Authenticate())
	incomingRouter.GET("/users", controller.GetUsers())
	incomingRouter.GET("/users/:user_id", controller.GetUser())
}
