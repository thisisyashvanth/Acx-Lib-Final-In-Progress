from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from security.dependency import get_current_user
from models.request_model import RequestStatus, RequestType

from services.request_service import (
    create_borrow_request,
    create_renew_request,
    create_return_request,
    review_request,
    check_and_flag_overdue,
    lift_expired_restrictions,
    get_all_requests,
    get_my_requests,
)


router = APIRouter(prefix="/request", tags=["Requests"])


# ================================
# ✅ USER: CREATE REQUESTS
# ================================
@router.post("/borrow/{book_id}")
def request_borrow(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Lift restriction if expired before checking
    lift_expired_restrictions(db)
    try:
        return create_borrow_request(book_id, db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/renew/{borrow_id}")
def request_renew(borrow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return create_renew_request(borrow_id, db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return/{borrow_id}")
def request_return(borrow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return create_return_request(borrow_id, db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# ✅ HR: REVIEW REQUEST
# ================================
@router.post("/{request_id}/review")
def review_request_endpoint(
    request_id: int,
    approve: bool,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can review requests")

    try:
        return review_request(request_id, approve, db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# ✅ HR: OVERDUE CHECK
# HR calls this every Tuesday to flag overdue books and restrict users
# ================================
@router.post("/admin/check-overdue")
def check_overdue(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can run overdue checks")

    try:
        return check_and_flag_overdue(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# ✅ HR: LIFT EXPIRED RESTRICTIONS
# ================================
@router.post("/admin/lift-restrictions")
def lift_restrictions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can lift restrictions")

    try:
        return lift_expired_restrictions(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================================
# ✅ HR: GET ALL REQUESTS
# ================================
@router.get("/requests")
def get_all_requests_endpoint(
    status: RequestStatus | None = Query(default=None),
    request_type: RequestType | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view all requests")

    requests = get_all_requests(db, status, request_type)

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
            "remarks": r.remarks,
        }
        for r in requests
    ]


# ================================
# ✅ USER: GET MY REQUESTS
# ================================
@router.get("/my-requests")
def get_my_requests_endpoint(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    requests = get_my_requests(db, user)

    return [
        {
            "request_id": r.id,
            "book_name": r.book.title,
            "request_type": r.request_type,
            "status": r.status,
            "requested_at": r.requested_at,
            "reviewed_at": r.reviewed_at,
            "remarks": r.remarks,
        }
        for r in requests
    ]