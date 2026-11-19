from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment
from app.schemas import CommentCreate, CommentRead, CommentUpdate

router = APIRouter(prefix="/v1/comments", tags=["comments"])


@router.get("", response_model=list[CommentRead])
def list_comments(
    task_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Comment).order_by(Comment.id)
    if task_id is not None:
        stmt = stmt.where(Comment.task_id == task_id)
    return db.scalars(stmt).all()


@router.get("/{comment_id}", response_model=CommentRead)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    comment = Comment(**payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.patch("/{comment_id}", response_model=CommentRead)
def update_comment(comment_id: int, payload: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
