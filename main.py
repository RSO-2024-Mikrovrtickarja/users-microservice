import uvicorn
from app.endpoints import users_app


if __name__ == "__main__":
    uvicorn.run(users_app, host="0.0.0.0", port=8002)
