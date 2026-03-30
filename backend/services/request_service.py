from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from models.borrow_model import BorrowRecord
from models.book_model import Book
from models.request_model import RequestStatus, RequestType, Requests


# 🔹 CONFIG (you can move this to settings later)
DEFAULT_BORROW_DAYS = 14
MAX_RENEWALS = 2


def create_request(request, db: Session, user):

    # ❗ Check for existing pending request
    existing_request = db.query(Requests).filter(
        Requests.user_id == user.id,
        Requests.book_id == request.book_id,
        Requests.status == RequestStatus.PENDING
    ).first()

    if existing_request:
        raise Exception("You already have a pending request for this book")

    # ❗ Additional smart checks based on request type

    # Check active borrow
    active_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user.id,
        BorrowRecord.book_id == request.book_id,
        BorrowRecord.returned_date.is_(None)
    ).first()

    # 🚫 If BORROW → user should NOT already have the book
    if request.request_type == RequestType.BORROW and active_borrow:
        raise Exception("You have already borrowed this book")

    # 🚫 If RETURN / RENEW → user MUST have active borrow
    if request.request_type in [RequestType.RETURN, RequestType.RENEW] and not active_borrow:
        raise Exception("No active borrow found for this book")

    # 🚫 Prevent multiple renew requests
    if request.request_type == RequestType.RENEW:
        if active_borrow.renewal_count >= MAX_RENEWALS:
            raise Exception("Max renewals already reached")

    # ✅ Create request
    new_request = Requests(
        user_id=user.id,
        book_id=request.book_id,
        request_type=request.request_type,
        status=RequestStatus.PENDING
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "id": new_request.id,
        "message": "Request created successfully"
    }


# ✅ Review Request (HR)
def review_request(request_id: int, review, db: Session, hr_user):
    req = db.query(Requests).filter(Requests.id == request_id).first()

    if not req:
        raise Exception("Request not found")

    if req.status != RequestStatus.PENDING:
        raise Exception("Already processed")

    req.status = review.status
    req.reviewed_by = hr_user.id
    req.reviewed_at = datetime.now(timezone.utc)
    req.remarks = review.remarks

    if review.status == RequestStatus.APPROVED:

        if req.request_type == RequestType.BORROW:
            _handle_borrow(req, db)

        elif req.request_type == RequestType.RETURN:
            _handle_return(req, db)

        elif req.request_type == RequestType.RENEW:
            _handle_renew(req, db)

    db.commit()
    db.refresh(req)

    return {
        "id": req.id,
        "status": req.status,
        "message": f"Request {req.status.lower()}"
    }


# 🔁 BORROW
def _handle_borrow(req, db: Session):
    book = db.query(Book).filter(Book.id == req.book_id).first()

    if not book:
        raise Exception("Book not found")

    if book.available_copies <= 0:
        raise Exception("No copies available")

    # Prevent duplicate active borrow
    existing = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == req.user_id,
        BorrowRecord.book_id == req.book_id,
        BorrowRecord.returned_date.is_(None)
    ).first()

    if existing:
        raise Exception("Book already borrowed")

    record = BorrowRecord(
        user_id=req.user_id,
        book_id=req.book_id,
        issue_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=DEFAULT_BORROW_DAYS),
        status="borrowed"
    )

    book.available_copies -= 1

    db.add(record)


# 🔁 RETURN
def _handle_return(req, db: Session):
    record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == req.user_id,
        BorrowRecord.book_id == req.book_id,
        BorrowRecord.returned_date.is_(None)
    ).first()

    if not record:
        raise Exception("No active borrow found")

    record.returned_date = datetime.now(timezone.utc)
    record.status = "returned"

    book = db.query(Book).filter(Book.id == req.book_id).first()
    book.available_copies += 1


# 🔁 RENEW
def _handle_renew(req, db: Session):
    record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == req.user_id,
        BorrowRecord.book_id == req.book_id,
        BorrowRecord.returned_date.is_(None)
    ).first()

    if not record:
        raise Exception("No active borrow found")

    if record.renewal_count >= MAX_RENEWALS:
        raise Exception("Max renewals reached")

    record.due_date += timedelta(days=DEFAULT_BORROW_DAYS)
    record.renewal_count += 1


# ✅ Get all requests (HR)
def get_all_requests(db: Session):
    return db.query(Requests).order_by(
        Requests.requested_at.desc()
    ).all()


# ✅ Get single request
def get_request(request_id: int, db: Session):
    req = db.query(Requests).filter(
        Requests.id == request_id
    ).first()

    if not req:
        raise Exception("Request not found")
    
    return req


# # ✅ Get user requests
# def get_user_requests(user_id: int, db: Session):
#     return db.query(Requests).filter(
#         Requests.user_id == user_id
#     ).order_by(Requests.requested_at.desc()).all()