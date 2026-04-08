from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from models.borrow_model import BorrowRecord, TransactionStatus
from models.book_model import Book
from models.request_model import RequestStatus, RequestType, Requests
from models.user_model import User


MAX_RENEWALS = 1
RESTRICTION_DAYS = 30


def _get_fourth_tuesday(from_date: datetime) -> datetime:
    """Returns the 4th Tuesday on or after from_date."""
    d = from_date.replace(hour=0, minute=0, second=0, microsecond=0)
    days_until_tuesday = (1 - d.weekday()) % 7
    first_tuesday = d + timedelta(days=days_until_tuesday)
    fourth_tuesday = first_tuesday + timedelta(weeks=4)
    return fourth_tuesday


# ACTUAL LOGIC
# def _is_tuesday_second_half() -> bool:
#     """Returns True if it's Tuesday between 12:00 PM and 6:00 PM UTC."""
#     now = datetime.now(timezone.utc)
#     return now.weekday() == 1 and 12 <= now.hour < 18


# TESTING
def _is_tuesday_second_half() -> bool:
    return True 


def create_borrow_request(book_id: int, db: Session, user):

    if not _is_tuesday_second_half():
        raise Exception("Borrow requests can only be made on Tuesdays between 12:00 PM and 6:00 PM")

    if user.is_restricted:
        raise Exception("You are restricted from borrowing books")

    existing_borrow = db.query(BorrowRecord).filter_by(
        user_id=user.id,
        status=TransactionStatus.ACTIVE
    ).first()

    if existing_borrow:
        raise Exception("You already have an active borrowed book")

    existing_request = db.query(Requests).filter_by(
        user_id=user.id,
        book_id=book_id,
        request_type=RequestType.BORROW,
        status=RequestStatus.PENDING
    ).first()

    if existing_request:
        raise Exception("Borrow request already pending for this book")

    book = db.query(Book).filter_by(id=book_id).first()
    if not book:
        raise Exception("Book not found")

    req = Requests(
        user_id=user.id,
        book_id=book_id,
        request_type=RequestType.BORROW
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Borrow request created", "request_id": req.id}


def create_renew_request(borrow_id: int, db: Session, user):

    if not _is_tuesday_second_half():
        raise Exception("Renewals can only be requested on Tuesdays after 12:00 PM")

    borrow = db.query(BorrowRecord).filter_by(
        id=borrow_id,
        user_id=user.id
    ).first()

    if not borrow:
        raise Exception("Borrow record not found")

    if borrow.status != TransactionStatus.ACTIVE:
        raise Exception("Cannot renew this book")

    if borrow.renewal_count >= MAX_RENEWALS:
        raise Exception("Renewal limit reached. Please return the book.")

    existing_request = db.query(Requests).filter(
        Requests.user_id == user.id,
        Requests.borrow_id == borrow_id,
        Requests.status == RequestStatus.PENDING
    ).first()

    if existing_request:
        raise Exception(f"{existing_request.request_type.value} request already pending")

    req = Requests(
        user_id=user.id,
        book_id=borrow.book_id,
        borrow_id=borrow.id,
        request_type=RequestType.RENEW
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Renew request created", "request_id": req.id}


def create_return_request(borrow_id: int, db: Session, user):

    if not _is_tuesday_second_half():
        raise Exception("Returns can only be requested on Tuesdays after 12:00 PM")

    borrow = db.query(BorrowRecord).filter_by(
        id=borrow_id,
        user_id=user.id
    ).first()

    if not borrow:
        raise Exception("Borrow record not found")

    if borrow.status != TransactionStatus.ACTIVE:
        raise Exception("Already returned")

    existing_request = db.query(Requests).filter(
        Requests.user_id == user.id,
        Requests.borrow_id == borrow_id,
        Requests.status == RequestStatus.PENDING
    ).first()

    if existing_request:
        raise Exception(f"{existing_request.request_type.value} request already pending")

    req = Requests(
        user_id=user.id,
        book_id=borrow.book_id,
        borrow_id=borrow.id,
        request_type=RequestType.RETURN
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Return request created", "request_id": req.id}


def check_and_flag_overdue(db: Session):
    """
    Marks overdue borrows and restricts employees who failed to
    renew or return by their due date.
    HR calls this endpoint every Tuesday.
    """
    now = datetime.now(timezone.utc)

    overdue_records = db.query(BorrowRecord).filter(
        BorrowRecord.status == TransactionStatus.ACTIVE,
        BorrowRecord.due_date < now
    ).all()

    restricted_users = []

    for record in overdue_records:
        record.status = TransactionStatus.OVERDUE

        user = db.query(User).filter_by(id=record.user_id).first()
        if user and not user.is_restricted:
            user.is_restricted = True
            user.restricted_until = now + timedelta(days=RESTRICTION_DAYS)
            restricted_users.append(user.name)

    db.commit()

    return {
        "overdue_count": len(overdue_records),
        "restricted_users": restricted_users
    }


def lift_expired_restrictions(db: Session):
    """
    Lifts restrictions for users whose restriction period has ended.
    HR calls this endpoint or it runs automatically on login.
    """
    now = datetime.now(timezone.utc)

    expired = db.query(User).filter(
        User.is_restricted == True,
        User.restricted_until <= now
    ).all()

    for user in expired:
        user.is_restricted = False
        user.restricted_until = None

    db.commit()

    return {"lifted_count": len(expired)}


def review_request(request_id: int, approve: bool, remarks: str | None, db: Session, hr_user):

    if not _is_tuesday_second_half():
        raise Exception("Requests can only be reviewed on Tuesdays between 12:00 PM and 6:00 PM")

    req = db.query(Requests).filter_by(id=request_id).first()

    if not req:
        raise Exception("Request not found")

    if req.status != RequestStatus.PENDING:
        raise Exception("Already reviewed")

    now = datetime.now(timezone.utc)

    if not approve:
        if not remarks:
            raise Exception("Remarks are required for rejection")

        req.status = RequestStatus.REJECTED
        req.remarks = remarks
        req.reviewed_by = hr_user.id
        req.reviewed_at = now
        db.commit()
        return {"message": "Request rejected"}

    if req.request_type == RequestType.BORROW:
        _approve_borrow(req, db, hr_user, now)

    elif req.request_type == RequestType.RENEW:
        _approve_renew(req, db)

    elif req.request_type == RequestType.RETURN:
        _approve_return(req, db)

    req.status = RequestStatus.APPROVED
    req.reviewed_by = hr_user.id
    req.reviewed_at = now

    if remarks:
        req.remarks = remarks

    db.commit()

    return {"message": "Request approved"}


def _approve_borrow(req, db: Session, hr_user, now: datetime):

    book = db.query(Book).filter_by(id=req.book_id).with_for_update().first()

    if not book:
        raise Exception("Book not found")

    if book.available_copies <= 0:
        req.status = RequestStatus.REJECTED
        req.reviewed_by = hr_user.id
        req.reviewed_at = now
        req.remarks = "Auto-rejected: No copies available"
        db.commit()
        raise Exception("No copies available. Request auto-rejected.")

    due_date = _get_fourth_tuesday(now)

    borrow = BorrowRecord(
        user_id=req.user_id,
        book_id=req.book_id,
        issue_date=now,
        due_date=due_date,
        renewal_count=0
    )
    db.add(borrow)
    book.available_copies -= 1

    db.query(Requests).filter(
        Requests.user_id == req.user_id,
        Requests.id != req.id,
        Requests.request_type == RequestType.BORROW,
        Requests.status == RequestStatus.PENDING
    ).update(
        {
            Requests.status: RequestStatus.REJECTED,
            Requests.reviewed_by: hr_user.id,
            Requests.reviewed_at: now,
            Requests.remarks: "Auto-rejected: Another borrow request was approved"
        },
        synchronize_session=False
    )


def _approve_renew(req, db: Session):

    borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

    if not borrow:
        raise Exception("Borrow record not found")

    if borrow.renewal_count >= MAX_RENEWALS:
        raise Exception("Renewal limit reached")

    borrow.due_date = _get_fourth_tuesday(borrow.due_date)
    borrow.renewal_count += 1


def _approve_return(req, db: Session):

    borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

    if not borrow:
        raise Exception("Borrow record not found")

    borrow.status = TransactionStatus.RETURNED
    borrow.returned_date = datetime.now(timezone.utc)

    book = db.query(Book).filter_by(id=borrow.book_id).first()
    if book:
        book.available_copies += 1


def get_all_requests(db: Session, status=None, request_type=None):
    query = db.query(Requests)

    if status:
        query = query.filter(Requests.status == status)

    if request_type:
        query = query.filter(Requests.request_type == request_type)

    return query.order_by(Requests.requested_at.desc()).all()


def get_my_requests(db: Session, user):
    return db.query(Requests).filter(Requests.user_id == user.id, Requests.status != RequestStatus.PENDING).order_by(Requests.requested_at.desc()).all()