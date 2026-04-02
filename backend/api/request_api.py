from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import get_current_user
from models.borrow_model import BorrowRecord, TransactionStatus
from models.book_model import Book
from models.request_model import RequestStatus, RequestType, Requests
from datetime import datetime, timedelta, timezone



router = APIRouter(prefix="/request", tags=["Requests"])


def get_pending_borrow_action(db: Session, user_id: int, borrow_id: int):
    return db.query(Requests).filter(
        Requests.user_id == user_id,
        Requests.borrow_id == borrow_id,
        Requests.status == RequestStatus.PENDING,
        Requests.request_type.in_([RequestType.RENEW, RequestType.RETURN])
    ).first()


@router.post("/borrow/{book_id}")
def request_borrow(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    if user.is_restricted:
        raise HTTPException(status_code=403, detail="User is restricted")

    # ✅ check active borrow
    existing_borrow = db.query(BorrowRecord).filter_by(
        user_id=user.id,
        status=TransactionStatus.ACTIVE
    ).first()

    if existing_borrow:
        raise HTTPException(status_code=400, detail="Already borrowed a book")

    existing_request = db.query(Requests).filter_by(
        user_id=user.id,
        book_id=book_id,
        request_type=RequestType.BORROW,
        status=RequestStatus.PENDING
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Borrow request already pending for this book"
        )

    # check book exists
    book = db.query(Book).filter_by(id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    req = Requests(
        user_id=user.id,
        book_id=book_id,
        request_type=RequestType.BORROW
    )



    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Borrow request created", "request_id": req.id}


@router.post("/renew/{borrow_id}")
def request_renew(borrow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    borrow = db.query(BorrowRecord).filter_by(
        id=borrow_id,
        user_id=user.id
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow Record Not Found.")

    if borrow.status != TransactionStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Cannot Renew This Book.")

    if borrow.renewal_count >= 1:
        raise HTTPException(
            status_code=400,
            detail="Renewal Limit Reached. Please Return The Book."
        )

    pending_request = get_pending_borrow_action(db, user.id, borrow.id)
    if pending_request:
        raise HTTPException(
            status_code=400,
            detail=f"{pending_request.request_type.value.title()} request already pending for this book."
        )

    req = Requests(
        user_id=user.id,
        book_id=borrow.book_id,
        borrow_id=borrow.id,
        request_type=RequestType.RENEW
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Renew Request Created", "request_id": req.id}


@router.post("/return/{borrow_id}")
def request_return(borrow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    borrow = db.query(BorrowRecord).filter_by(
        id=borrow_id,
        user_id=user.id
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow Record Not Found.")

    if borrow.status != TransactionStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Already Returned.")

    pending_request = get_pending_borrow_action(db, user.id, borrow.id)
    if pending_request:
        raise HTTPException(
            status_code=400,
            detail=f"{pending_request.request_type.value.title()} request already pending for this book."
        )

    req = Requests(
        user_id=user.id,
        book_id=borrow.book_id,
        borrow_id=borrow.id,
        request_type=RequestType.RETURN
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    return {"message": "Return Request Created", "request_id": req.id}



# @router.post("/{request_id}/review")
# def review_request(
#     request_id: int,
#     approve: bool,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     if user.role != "HR":
#         raise HTTPException(status_code=403, detail="Only HR can review")

#     req = db.query(Requests).filter_by(id=request_id).first()
#     if not req:
#         raise HTTPException(status_code=404, detail="Request not found")

#     if req.status != RequestStatus.PENDING:
#         raise HTTPException(status_code=400, detail="Already reviewed")

#     if not approve:
#         req.status = RequestStatus.REJECTED

#     else:
#         req.status = RequestStatus.APPROVED

#         if req.request_type == RequestType.BORROW:

#             book = db.query(Book).filter_by(id=req.book_id).first()

#             if book.available_copies <= 0:
#                 raise HTTPException(status_code=400, detail="No copies available")

#             due_date = datetime.now(timezone.utc) + timedelta(days=28)

#             borrow = BorrowRecord(
#                 user_id=req.user_id,
#                 book_id=req.book_id,
#                 due_date=due_date,
#                 renewal_count=0
#             )

#             db.add(borrow)
#             book.available_copies -= 1

#         elif req.request_type == RequestType.RENEW:

#             borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

#             # ✅ enforce again at approval level (important!)
#             if borrow.renewal_count >= 1:
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Renewal limit reached"
#                 )

#             borrow.due_date += timedelta(days=28)
#             borrow.renewal_count += 1

#         elif req.request_type == RequestType.RETURN:

#             borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

#             borrow.status = TransactionStatus.RETURNED
#             borrow.returned_date = datetime.now(timezone.utc)

#             book = db.query(Book).filter_by(id=borrow.book_id).first()
#             book.available_copies += 1

#     req.reviewed_by = user.id
#     req.reviewed_at = datetime.now(timezone.utc)

#     db.commit()

#     return {"message": f"Request {'approved' if approve else 'rejected'}"}





@router.post("/{request_id}/review")
def review_request(
    request_id: int,
    approve: bool,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can review")

    req = db.query(Requests).filter_by(id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if req.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Already reviewed")

    now = datetime.now(timezone.utc)

    # ❌ If rejected manually
    if not approve:
        req.status = RequestStatus.REJECTED
        req.reviewed_by = user.id
        req.reviewed_at = now

        db.commit()
        return {"message": "Request rejected"}

    # ✅ APPROVAL FLOW
    if req.request_type == RequestType.BORROW:

        # 🔒 Lock book row (prevents race condition)
        book = db.query(Book).filter_by(id=req.book_id).with_for_update().first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # ❌ No copies → reject this request
        if book.available_copies <= 0:
            req.status = RequestStatus.REJECTED
            req.reviewed_by = user.id
            req.reviewed_at = now
            req.remarks = "Auto-rejected: No copies available"

            db.commit()
            return {"message": "No copies available. Request auto-rejected."}

        # ✅ Approve request
        req.status = RequestStatus.APPROVED

        due_date = now + timedelta(days=28)

        borrow = BorrowRecord(
            user_id=req.user_id,
            book_id=req.book_id,
            due_date=due_date,
            renewal_count=0
        )

        db.add(borrow)

        # 📉 Reduce copies
        book.available_copies -= 1

        # 🚨 Auto reject remaining pending requests
        if book.available_copies == 0:
            db.query(Requests).filter(
                Requests.book_id == req.book_id,
                Requests.status == RequestStatus.PENDING
            ).update(
                {
                    Requests.status: RequestStatus.REJECTED,
                    Requests.reviewed_by: user.id,
                    Requests.reviewed_at: now,
                    Requests.remarks: "Auto-rejected: No copies available"
                },
                synchronize_session=False
            )

    elif req.request_type == RequestType.RENEW:

        borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

        if not borrow:
            raise HTTPException(status_code=404, detail="Borrow record not found")

        if borrow.renewal_count >= 1:
            raise HTTPException(status_code=400, detail="Renewal limit reached")

        borrow.due_date += timedelta(days=28)
        borrow.renewal_count += 1

        req.status = RequestStatus.APPROVED

    elif req.request_type == RequestType.RETURN:

        borrow = db.query(BorrowRecord).filter_by(id=req.borrow_id).first()

        if not borrow:
            raise HTTPException(status_code=404, detail="Borrow record not found")

        borrow.status = TransactionStatus.RETURNED
        borrow.returned_date = now

        book = db.query(Book).filter_by(id=borrow.book_id).first()
        if book:
            book.available_copies += 1

        req.status = RequestStatus.APPROVED

    # ✅ Common review metadata
    req.reviewed_by = user.id
    req.reviewed_at = now

    db.commit()

    return {"message": "Request approved"}




from fastapi import Query

@router.get("/requests")
def get_all_requests(
    status: RequestStatus | None = Query(default=None),
    request_type: RequestType | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # ✅ Only HR allowed
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view requests")

    query = db.query(Requests)

    # ✅ optional filters
    if status:
        query = query.filter(Requests.status == status)

    if request_type:
        query = query.filter(Requests.request_type == request_type)

    requests = query.order_by(Requests.requested_at.desc()).all()

    # simple response
    return [
        {
            "request_id": r.id,
            "employee_id": r.user.employee_id,
            "employee_name": r.user.name,
            "book_id": r.book_id,
            "book_name": r.book.title,
            "request_type": r.request_type,
            "status": r.status,
            "requested_at": r.requested_at,
            "reviewed_at": r.reviewed_at,
            "remarks": r.remarks
        }
        for r in requests
    ]
