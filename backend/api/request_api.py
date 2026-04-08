from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from security.dependency import get_current_user, require_hr
from models.request_model import RequestStatus, RequestType
from services.request_service import create_borrow_request, create_renew_request, create_return_request, review_request, check_and_flag_overdue, lift_expired_restrictions, get_all_requests, get_my_requests
from schemas.request_schema import ReviewRequestBody


router = APIRouter(prefix="/request", tags=["Requests"])


@router.post("/borrow/{book_id}")
def request_borrow(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
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


@router.post("/{request_id}/review")
def review_request_endpoint(request_id: int, body: ReviewRequestBody, db: Session = Depends(get_db), user=Depends(require_hr)):
    try:
        return review_request(request_id, body.approve, body.remarks, db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/check-overdue")
def check_overdue(db: Session = Depends(get_db), hr=Depends(require_hr)):
    try:
        return check_and_flag_overdue(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/lift-restrictions")
def lift_restrictions(db: Session = Depends(get_db), hr=Depends(require_hr)):
    try:
        return lift_expired_restrictions(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests")
def get_all_requests(status: RequestStatus | None = Query(default=None), request_type: RequestType | None = Query(default=None), db: Session = Depends(get_db), hr=Depends(require_hr)):

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


@router.get("/my-requests")
def get_my_requests_endpoint(db: Session = Depends(get_db), user=Depends(get_current_user)):
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