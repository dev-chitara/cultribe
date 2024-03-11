import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Cultribe API",
    description="Cultribe swagger documentation",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        access_log=True,
        reload=True
    )
