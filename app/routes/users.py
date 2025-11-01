"""
User management endpoints.
Handles CRUD operations for users within a tenant.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..auth.jwt import get_password_hash
from ..auth.middleware import get_current_user, require_admin


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse])
def get_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get all users in current tenant.
    
    Permission: Admin only
    
    Returns:
        List of users in admin's organization
    """
    users = db.query(User).filter(
        User.tenant_id == current_user.tenant_id
    ).all()
    
    return users


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Permission: All authenticated users
    
    Returns:
        Current user details
    """
    return current_user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Create new user in current tenant.
    
    Permission: Admin only
    
    Args:
        user_data: User information
        
    Returns:
        Created user details
        
    Raises:
        HTTPException 400 if username already exists in tenant
    """
    # Check username availability in this tenant
    existing = db.query(User).filter(
        User.username == user_data.username,
        User.tenant_id == current_user.tenant_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_data.username}' already exists in your organization"
        )
    
    # Create user
    user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role,
        tenant_id=current_user.tenant_id,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Update user information.
    
    Permission: Admin only
    
    Args:
        user_id: User ID to update
        user_data: Fields to update
        
    Returns:
        Updated user details
        
    Raises:
        HTTPException 404 if user not found
        HTTPException 403 if trying to update user from different tenant
    """
    # Find user with tenant verification
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id and user_data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Update only provided fields
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Delete user from tenant.
    
    Permission: Admin only
    
    Args:
        user_id: User ID to delete
        
    Raises:
        HTTPException 404 if user not found
        HTTPException 400 if trying to delete self
    """
    # Find user with tenant verification
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return None
