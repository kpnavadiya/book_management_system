"""
Tenant management endpoints.
Handles organization registration and management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.tenant import Tenant
from ..models.user import User, UserRole
from ..schemas.tenant import TenantCreate, TenantResponse, TenantUpdate
from ..auth.jwt import get_password_hash
from ..auth.middleware import get_current_user, require_admin
from ..utils.helpers import generate_tenant_url


router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.post("/register", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def register_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new organization/tenant.
    
    Process:
    1. Validate subdomain is available
    2. Create tenant record
    3. Create default admin user
    4. Return tenant info with access URL
    
    This is a public endpoint for new organization signup.
    """
    # Check subdomain availability
    existing = db.query(Tenant).filter(
        Tenant.subdomain == tenant_data.subdomain
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subdomain '{tenant_data.subdomain}' is already taken"
        )
    
    try:
        # Create tenant
        tenant = Tenant(
            name=tenant_data.name,
            subdomain=tenant_data.subdomain,
            is_active=True
        )
        db.add(tenant)
        db.flush()  # To generate tenant.id without commit yet

        # Create default admin user with password truncated properly
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("ChangeMe123!"[:72]),  # Truncate if necessary
            role=UserRole.ADMIN,
            tenant_id=tenant.id,
            is_active=True
        )
        db.add(admin_user)
        db.commit()  # Commit both tenant and user atomically
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tenant and admin user"
        )
    
    # Generate response with URL
    response = TenantResponse(
        id=tenant.id,
        name=tenant.name,
        subdomain=tenant.subdomain,
        is_active=tenant.is_active,
        created_at=tenant.created_at,
        url=generate_tenant_url(tenant.subdomain)
    )
    
    return response



@router.get("/me", response_model=TenantResponse)
def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's tenant information.
    
    Returns:
        Tenant details for authenticated user's organization
    """
    print(f"[DEBUG] Current user: id={current_user.id}, tenant_id={current_user.tenant_id}, username={current_user.username}")
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    # print("Current tenant(routes/tenants.py):", tenant)
    if not tenant:
        print(f"[DEBUG] Tenant not found for tenant_id: {current_user.tenant_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    print(f"[DEBUG] Tenant found: id={tenant.id}, name={tenant.name}, subdomain={tenant.subdomain}")
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        subdomain=tenant.subdomain,
        is_active=tenant.is_active,
        created_at=tenant.created_at,
        url=generate_tenant_url(tenant.subdomain)
    )


@router.put("/me", response_model=TenantResponse)
def update_current_tenant(
    tenant_update: TenantUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Update current tenant information.
    
    Permission: Admin only
    
    Args:
        tenant_update: Fields to update
        
    Returns:
        Updated tenant information
    """
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Update only provided fields
    update_data = tenant_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tenant, field, value)
    
    db.commit()
    db.refresh(tenant)
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        subdomain=tenant.subdomain,
        is_active=tenant.is_active,
        created_at=tenant.created_at,
        url=generate_tenant_url(tenant.subdomain)
    )
