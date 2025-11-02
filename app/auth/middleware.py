"""
Authentication middleware and dependency functions.
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models.user import User, UserRole
from ..models.tenant import Tenant
from .jwt import decode_token, verify_token_type, extract_user_from_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    print(f"[DEBUG] Received credentials: {credentials}")
    token = credentials.credentials

    try:
        payload = decode_token(token)
        print(f"[DEBUG] Decoded token payload: {payload}")
    except Exception as e:
        print(f"[DEBUG] Token decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not payload:
        print("[DEBUG] Empty payload after decoding token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Further debugging on values extracted
    user_id, tenant_id, role = extract_user_from_token(payload)
    print(f"[DEBUG] Extracted user_id={user_id}, tenant_id={tenant_id}, role={role}")

    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id
    ).first()

    if not user:
        print("[DEBUG] User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        print("[DEBUG] User is inactive")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    print(f"[DEBUG] User found: username={user.username}, last_login={user.last_login}")
    user.last_login = datetime.utcnow()
    db.commit()

    return user



def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(*allowed_roles: UserRole):
    """Dependency factory for role-based access control."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker


require_admin = require_role(UserRole.ADMIN)
require_librarian = require_role(UserRole.ADMIN, UserRole.LIBRARIAN)
require_member = require_role(UserRole.ADMIN, UserRole.LIBRARIAN, UserRole.MEMBER)


def get_tenant_from_request(request: Request, db: Session = Depends(get_db)) -> Optional[Tenant]:
    """Extract tenant from request URL."""
    host = request.headers.get("host", "")
    
    if "." in host:
        subdomain = host.split(".")[0]
        if subdomain not in ["www", "api", "admin", "localhost"]:
            tenant = db.query(Tenant).filter(Tenant.subdomain == subdomain).first()
            if tenant:
                return tenant
    
    path = request.url.path
    if path.startswith("/tenant/"):
        parts = path.split("/")
        if len(parts) > 2:
            tenant_subdomain = parts[2]
            tenant = db.query(Tenant).filter(Tenant.subdomain == tenant_subdomain).first()
            if tenant:
                return tenant
    
    return None


def verify_tenant_access(
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[int] = None
) -> bool:
    """Verify user has access to specified tenant."""
    if tenant_id and current_user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this tenant's resources"
        )
    return True
