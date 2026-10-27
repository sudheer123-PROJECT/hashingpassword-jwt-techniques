from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base, engine, get_db
from models import User

from schemas import (
    UserRegister,
    UserLogin,
    UserUpdate,
    UserResponse,
    TokenResponse
)

from security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Login Project")

# Frontend will run on localhost:5500
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"]
)

bearer_scheme = HTTPBearer(auto_error=False)


# Home API
@app.get("/")
def home():
    return {"message": "Secure Login API is running"}


# 1. REGISTER API
@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserRegister, db: Session = Depends(get_db)):

    email = str(user.email).lower()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db.refresh(new_user)

    return new_user


# 2. LOGIN API
@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    email = str(user.email).lower()

    db_user = db.query(User).filter(
        User.email == email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = verify_password(
        user.password,
        db_user.hashed_password
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# JWT AUTHENTICATION DEPENDENCY
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = verify_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


# 3. PROTECTED PROFILE API
@app.get("/profile", response_model=UserResponse)
def profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# 4. UPDATE PROFILE API
@app.put("/profile", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user.username = data.username

    db.commit()
    db.refresh(current_user)

    return current_user


# 5. PROTECTED DASHBOARD API
@app.get("/dashboard")
def dashboard(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": f"Welcome {current_user.username}!",
        "status": "Authenticated successfully"
    }