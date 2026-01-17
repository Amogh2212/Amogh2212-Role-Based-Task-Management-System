from fastapi import HTTPException, status

ROLE_HIERARCHY = {
    "manager": 5,
    "senior_dev": 4,
    "developer": 3,
    "hr": 2,
    "intern": 1
}

def can_assign_task(assigner_role: str, assignee_role: str) -> bool:
    if assigner_role not in ROLE_HIERARCHY or assignee_role not in ROLE_HIERARCHY:
        return False

    return ROLE_HIERARCHY[assigner_role] > ROLE_HIERARCHY[assignee_role]

def check_assignment_permission(assigner_role: str, assignee_role: str):
    if not can_assign_task(assigner_role, assignee_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to assign tasks to this role"
        )
