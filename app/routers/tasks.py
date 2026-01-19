from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import get_current_user
from app.core.roles import check_assignment_permission

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/assign", response_model=TaskResponse)
def assign_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignee = db.query(User).filter(
        User.emp_id == task.assigned_to_emp_id
    ).first()

    if not assignee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned employee not found"
        )

    check_assignment_permission(
        assigner_role=current_user.role,
        assignee_role=assignee.role
    )

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        assigned_by=current_user.id,
        assigned_to=assignee.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/my-tasks", response_model=list[TaskResponse])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.assigned_to == current_user.id
    ).all()

    return tasks

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your assigned tasks"
        )

    if task_update.status:
        task.status = task_update.status

    db.commit()
    db.refresh(task)

    return task

@router.get("/all", response_model=list[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can view all tasks"
        )

    return db.query(Task).all()

