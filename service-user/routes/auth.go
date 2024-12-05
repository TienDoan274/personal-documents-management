package routes

import (
	"github.com/gin-gonic/gin"
	controller "service-user/controllers"

)

func AuthRoutes(incomingRouter *gin.Engine) {
	incomingRouter.POST("/user/signup", controller.Signup())
	incomingRouter.POST("/user/login", controller.Login())
}
