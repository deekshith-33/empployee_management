import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, require_admin
from core.security import create_access_token, hash_password, verify_password
from database.database import get_db
from models.models import User
from schema.schema import (
    Token,
    UserCreate,
    UserResponse,
    UserRole,
    UserRoleUpdate,
)

router = APIRouter(prefix="/users", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if the email is already registered
    existing_user = db.query(User).filter(User.email == str(user_in.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    # 2. Validate role & admin invite secret
    assigned_role = UserRole.EMPLOYEE.value

    if user_in.role == UserRole.ADMIN:
        expected_secret = os.getenv("ADMIN_SECRET_KEY")
        if not expected_secret or user_in.admin_secret != expected_secret:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing admin registration secret.",
            )
        assigned_role = UserRole.ADMIN.value

    # 3. Hash the plain-text password
    hashed_pwd = hash_password(user_in.password)

    # 4. Create and persist the user with the validated role
    new_user = User(
        email=str(user_in.email),
        hashed_password=hashed_pwd,
        role=assigned_role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 1. Find the user by username (OAuth2 form field standard uses 'username' for the email/ID)
    user = db.query(User).filter(User.email == form_data.username).first()

    # 2. Validate user existence and check password hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Create the JWT token with subject (email) and role claims
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Return the profile of the currently logged-in user."""
    return current_user


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Admin-only endpoint to promote or demote an existing user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.role = payload.role.value
    db.commit()
    db.refresh(user)
    return user