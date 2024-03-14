import uvicorn
from fastapi import FastAPI
from routers import users
from routers import posts
from routers import groups
from routers import comments
from routers import auth


app = FastAPI(
    title="Cultribe API",
    description="Cultribe swagger documentation",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)


app.include_router(users.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        access_log=True,
        reload=True
    )
