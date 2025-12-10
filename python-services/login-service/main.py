"""
Login Microservice - FastAPI
Handles user authentication and registration
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI(
    title="Login Microservice",
    description="User authentication and authorization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:1123",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Mock user database (in production, use real database)
MOCK_USERS = {
    "user@example.com": {
        "user_id": "u1001",
        "email": "user@example.com",
        "password": "password123",  # In production, use hashed passwords
        "firstName": "John",
        "lastName": "Doe"
    },
    "admin@example.com": {
        "user_id": "u1000",
        "email": "admin@example.com",
        "password": "admin123",
        "firstName": "Admin",
        "lastName": "User"
    }
}

# Mock sessions (in production, use Redis or database)
MOCK_SESSIONS = {}


class LoginRequest(BaseModel):
    username: str  # Actually email
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str


class LoginResponse(BaseModel):
    userId: str
    token: str
    email: str
    firstName: str
    lastName: str


class RegisterResponse(BaseModel):
    userId: str
    email: str
    firstName: str
    lastName: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {"service": "login-microservice", "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "login-microservice"}


@app.post("/login-microservice/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return session token
    """
    # Find user by email
    user = MOCK_USERS.get(request.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password (in production, use bcrypt)
    if user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate session token (in production, use JWT)
    token = f"token_{user['user_id']}_{datetime.now().timestamp()}"
    
    # Store session
    MOCK_SESSIONS[token] = {
        "user_id": user["user_id"],
        "email": user["email"],
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    
    return LoginResponse(
        userId=user["user_id"],
        token=token,
        email=user["email"],
        firstName=user["firstName"],
        lastName=user["lastName"]
    )


@app.post("/login-microservice/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    """
    Register a new user
    """
    # Check if user already exists
    if request.email in MOCK_USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
    # Generate user ID
    user_id = f"u{len(MOCK_USERS) + 1000}"
    
    # Create user (in production, hash password and save to database)
    MOCK_USERS[request.email] = {
        "user_id": user_id,
        "email": request.email,
        "password": request.password,  # In production, use bcrypt
        "firstName": request.firstName,
        "lastName": request.lastName
    }
    
    return RegisterResponse(
        userId=user_id,
        email=request.email,
        firstName=request.firstName,
        lastName=request.lastName
    )


@app.post("/login-microservice/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout user and invalidate session
    """
    token = credentials.credentials
    
    if token in MOCK_SESSIONS:
        del MOCK_SESSIONS[token]
    
    return {"message": "Logged out successfully"}


@app.get("/login-microservice/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify if a token is valid
    """
    token = credentials.credentials
    
    session = MOCK_SESSIONS.get(token)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Check if token expired
    if session["expires_at"] < datetime.now():
        del MOCK_SESSIONS[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    
    return {
        "valid": True,
        "userId": session["user_id"],
        "email": session["email"]
    }


@app.get("/login-microservice/user/{user_id}")
async def get_user(user_id: str):
    """
    Get user information by user ID
    """
    # Find user
    for email, user in MOCK_USERS.items():
        if user["user_id"] == user_id:
            return {
                "userId": user["user_id"],
                "email": user["email"],
                "firstName": user["firstName"],
                "lastName": user["lastName"]
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8085"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

