from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import redis.asyncio as redis
import os
import uuid
from typing import List, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import bcrypt
from datetime import datetime, timedelta

app = FastAPI(title="Take-Home Assignment API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configuration
SECRET_KEY = "dev-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)
security = HTTPBearer()

# Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
redis_client: Optional[redis.Redis] = None


@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = redis.Redis(
        host=redis_host, port=redis_port, decode_responses=True
    )
    # Create a default test user for development
    await create_default_user()


@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()


# Auth utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        try:
            password_bytes = plain_password.encode('utf-8')
            hash_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    except Exception:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username, "user_id": payload.get("user_id")}


async def create_user(username: str, password: str) -> bool:
    """Create a user in Redis. Returns True if created, False if already exists."""
    if not redis_client:
        return False
    user_exists = await redis_client.exists(f"user:{username}")
    if not user_exists:
        user_id = str(uuid.uuid4())
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
        hashed_password = hashed.decode('utf-8')
        await redis_client.hset(
            f"user:{username}",
            mapping={
                "user_id": user_id,
                "username": username,
                "hashed_password": hashed_password,
            },
        )
        return True
    return False


async def create_default_user():
    """Create default test users for development"""
    await create_user("testuser", "testpass123")
    await create_user("testuser2", "testpass123")


# Pydantic models
class TodoItem(BaseModel):
    id: str
    title: str
    completed: bool = False
    user_id: Optional[str] = None


class CreateTodoRequest(BaseModel):
    title: str


class UpdateTodoRequest(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Auth Routes
@app.post("/api/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        user_data = await redis_client.hgetall(f"user:{login_data.username}")
        if not user_data or not verify_password(login_data.password, user_data.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": login_data.username, "user_id": user_data.get("user_id")},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API Routes
@app.get("/")
async def root():
    return {"message": "Take-Home Assignment API", "status": "ok"}


@app.get("/health")
async def health():
    if redis_client:
        try:
            await redis_client.ping()
            return {"status": "healthy", "redis": "connected"}
        except Exception:
            return {"status": "unhealthy", "redis": "disconnected"}
    return {"status": "unhealthy", "redis": "not initialized"}


@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos(current_user: dict = Depends(get_current_user)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        keys = await redis_client.keys("todo:*")
        todos = []
        for key in keys:
            todo_data = await redis_client.hgetall(key)
            if todo_data:
                todos.append(
                    TodoItem(
                        id=todo_data["id"],
                        title=todo_data["title"],
                        completed=todo_data.get("completed", "false") == "true",
                        user_id=todo_data.get("user_id"),
                    )
                )
        return sorted(todos, key=lambda x: x.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/todos", response_model=TodoItem)
async def create_todo(todo: CreateTodoRequest, current_user: dict = Depends(get_current_user)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        todo_id = str(uuid.uuid4())
        key = f"todo:{todo_id}"
        user_id = current_user.get("user_id")

        await redis_client.hset(
            key,
            mapping={
                "id": todo_id,
                "title": todo.title,
                "completed": "false",
                "user_id": user_id,
            },
        )

        return TodoItem(id=todo_id, title=todo.title, completed=False, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: str, current_user: dict = Depends(get_current_user)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        key = f"todo:{todo_id}"
        todo_data = await redis_client.hgetall(key)

        if not todo_data:
            raise HTTPException(status_code=404, detail="Todo not found")

        return TodoItem(
            id=todo_data["id"],
            title=todo_data["title"],
            completed=todo_data.get("completed", "false") == "true",
            user_id=todo_data.get("user_id"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: str, update: UpdateTodoRequest, current_user: dict = Depends(get_current_user)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        key = f"todo:{todo_id}"
        todo_data = await redis_client.hgetall(key)

        if not todo_data:
            raise HTTPException(status_code=404, detail="Todo not found")

        if update.title is not None:
            await redis_client.hset(key, "title", update.title)
            todo_data["title"] = update.title

        if update.completed is not None:
            await redis_client.hset(key, "completed", str(update.completed).lower())
            todo_data["completed"] = str(update.completed).lower()

        return TodoItem(
            id=todo_data["id"],
            title=todo_data["title"],
            completed=todo_data.get("completed", "false") == "true",
            user_id=todo_data.get("user_id"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str, current_user: dict = Depends(get_current_user)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    try:
        key = f"todo:{todo_id}"
        result = await redis_client.delete(key)

        if result == 0:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
