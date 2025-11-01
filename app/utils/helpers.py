"""
Utility helper functions.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from ..config import settings
import re


def generate_tenant_url(subdomain: str) -> str:
    """Generate full URL for a tenant."""
    if settings.TENANT_URL_PATTERN == "subdomain":
        return f"https://{subdomain}.{settings.BASE_DOMAIN}"
    else:
        return f"https://{settings.BASE_DOMAIN}/tenant/{subdomain}"


def sanitize_string(text: str) -> str:
    """Remove potentially harmful characters from string."""
    if not text:
        return ""
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    return text.strip()


def format_datetime(dt: Optional[datetime], format_string: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """Format datetime object to string."""
    if dt is None:
        return None
    return dt.strftime(format_string)


def paginate_query(query, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Paginate SQLAlchemy query results."""
    page = max(1, page)
    page_size = min(page_size, settings.MAX_PAGE_SIZE)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    offset = (page - 1) * page_size
    
    items = query.offset(offset).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def normalize_isbn(isbn: str) -> str:
    """Normalize ISBN by removing formatting characters."""
    return isbn.replace('-', '').replace(' ', '').strip()


def calculate_token_expiry_seconds() -> int:
    """Calculate access token expiry in seconds."""
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
