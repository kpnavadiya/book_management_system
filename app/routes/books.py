"""
Book management endpoints.
Handles CRUD operations for books with tenant isolation.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.book import Book
from ..models.user import User
from ..schemas.book import BookCreate, BookUpdate, BookResponse
from ..auth.middleware import get_current_user, require_admin, require_librarian, require_member
from ..utils.helpers import paginate_query, normalize_isbn


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=List[BookResponse])
def get_books(
    current_user: User = Depends(require_member),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search by title or author")
):
    """
    Get all books for current user's tenant.
    
    Permission: All authenticated users (member, librarian, admin)
    
    Args:
        skip: Pagination offset
        limit: Number of results
        search: Optional search term
        
    Returns:
        List of books in tenant's library
    """
    # Base query with tenant isolation
    query = db.query(Book).filter(Book.tenant_id == current_user.tenant_id)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Book.title.ilike(search_term)) | (Book.author.ilike(search_term))
        )
    
    # Apply pagination
    books = query.offset(skip).limit(limit).all()
    
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    current_user: User = Depends(require_member),
    db: Session = Depends(get_db)
):
    """
    Get specific book by ID.
    
    Permission: All authenticated users
    Security: Automatically verifies book belongs to user's tenant
    
    Args:
        book_id: Book ID to retrieve
        
    Returns:
        Book details
        
    Raises:
        HTTPException 404 if book not found or not in user's tenant
    """
    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == current_user.tenant_id
    ).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    current_user: User = Depends(require_librarian),
    db: Session = Depends(get_db)
):
    """
    Add new book to tenant's collection.
    
    Permission: Librarian or Admin only
    
    Args:
        book_data: Book information
        
    Returns:
        Created book details
        
    Raises:
        HTTPException 400 if ISBN already exists in tenant
    """
    # Normalize ISBN
    normalized_isbn = normalize_isbn(book_data.isbn)
    
    # Check if ISBN already exists in this tenant
    existing = db.query(Book).filter(
        Book.isbn == normalized_isbn,
        Book.tenant_id == current_user.tenant_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ISBN {normalized_isbn} already exists in your library"
        )
    
    # Create book
    book = Book(
        title=book_data.title,
        author=book_data.author,
        isbn=normalized_isbn,
        description=book_data.description,
        quantity=book_data.quantity,
        tenant_id=current_user.tenant_id,
        created_by=current_user.id
    )
    
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(require_librarian),
    db: Session = Depends(get_db)
):
    """
    Update existing book.
    
    Permission: Librarian or Admin only
    Security: Verifies book belongs to user's tenant
    
    Args:
        book_id: Book ID to update
        book_data: Fields to update
        
    Returns:
        Updated book details
        
    Raises:
        HTTPException 404 if book not found
        HTTPException 400 if ISBN conflict
    """
    # Find book with tenant verification
    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == current_user.tenant_id
    ).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Update only provided fields
    update_data = book_data.dict(exclude_unset=True)
    
    # If ISBN is being updated, check uniqueness
    if "isbn" in update_data:
        normalized_isbn = normalize_isbn(update_data["isbn"])
        existing = db.query(Book).filter(
            Book.isbn == normalized_isbn,
            Book.tenant_id == current_user.tenant_id,
            Book.id != book_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Another book with ISBN {normalized_isbn} already exists"
            )
        
        update_data["isbn"] = normalized_isbn
    
    # Apply updates
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Delete book from collection.
    
    Permission: Admin only
    Security: Verifies book belongs to user's tenant
    
    Args:
        book_id: Book ID to delete
        
    Raises:
        HTTPException 404 if book not found
    """
    book = db.query(Book).filter(
        Book.id == book_id,
        Book.tenant_id == current_user.tenant_id
    ).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.delete(book)
    db.commit()
    
    return None
