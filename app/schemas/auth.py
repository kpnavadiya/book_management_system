from pydantic import BaseModel, Field, constr


class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=100)
    password: constr(min_length=8, max_length=72)
    tenant_subdomain: constr(strip_whitespace=True, min_length=1) = Field(..., description="Tenant organization subdomain")


class ChangePasswordRequest(BaseModel):
    old_password: constr(min_length=8, max_length=72)
    new_password: constr(min_length=8, max_length=72)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token to obtain a new access token")
