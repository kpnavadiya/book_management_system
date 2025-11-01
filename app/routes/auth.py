"""
Authentication endpoints.
Handles login, token refresh, and logout.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.tenant import Tenant
from ..schemas.auth import LoginRequest, Token, RefreshTokenRequest, ChangePasswordRequest
from ..auth.jwt import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
    extract_user_from_token
)
from ..auth.middleware import get_current_user
from ..utils.helpers import calculate_token_expiry_seconds


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.
    
    Process:
    1. Find tenant by subdomain
    2. Find user within that tenant
    3. Verify password
    4. Generate access and refresh tokens
    
    Args:
        login_data: Username, password, and tenant subdomain
        
    Returns:
        Access token and refresh token
        
    Raises:
        HTTPException 401 if credentials invalid
        HTTPException 404 if tenant not found
    """
    # Find tenant
    tenant = db.query(Tenant).filter(
        Tenant.subdomain == login_data.tenant_subdomain
    ).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{login_data.tenant_subdomain}' not found"
        )
    
    if not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization is inactive"
        )
    
    # Find user in tenant
    user = db.query(User).filter(
        User.username == login_data.username,
        User.tenant_id == tenant.id
    ).first()
    
    # Verify password
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create token payload
    token_data = {
        "sub": user.id,
        "tenant_id": tenant.id,
        "role": user.role.value
    }
    
    # Generate tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=calculate_token_expiry_seconds()
    )


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token.
    
    Process:
    1. Decode and validate refresh token
    2. Verify user still exists
    3. Generate new token pair
    
    Args:
        refresh_data: Refresh token
        
    Returns:
        New access token and refresh token
        
    Raises:
        HTTPException 401 if refresh token invalid
    """
    # Decode refresh token
    payload = decode_token(refresh_data.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify token type
    verify_token_type(payload, "refresh")
    
    # Extract user info
    user_id, tenant_id, role = extract_user_from_token(payload)
    
    # Verify user still exists and is active
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists or is inactive"
        )
    
    # Generate new tokens
    token_data = {
        "sub": user.id,
        "tenant_id": tenant_id,
        "role": user.role.value
    }
    
    access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=calculate_token_expiry_seconds()
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user.
    
    Note: Since JWT tokens are stateless, true server-side invalidation
    requires a token blacklist (e.g., Redis). For now, client should
    delete tokens from storage.
    
    In production, add token to blacklist here.
    """
    # TODO: Add token to blacklist in Redis
    # redis_client.setex(f"blacklist:{token}", ttl, "1")
    return None


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.
    
    Args:
        password_data: Old and new passwords
        
    Returns:
        Success message
        
    Raises:
        HTTPException 401 if old password incorrect
    """
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
