# app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register_user(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == payload.email).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    # 2. Hash password
    hashed_password = get_password_hash(payload.password)

    # 3. Create user object
    new_user = models.User(
        username=payload.username, email=payload.email, password_hash=hashed_password
    )

    # 4. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Return safe response
    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post(
    "/login", response_model=schemas.TokenResponse, status_code=status.HTTP_200_OK
)
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. Fetch user by email
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # 2. Verify password
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # 3. Create JWT token
    access_token = create_access_token(user.id)

    # 4. Return token response
    return {"access_token": access_token, "token_type": "Bearer", "expires_in": 3600}
