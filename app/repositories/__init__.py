from app.repositories.student import student_repo
from app.repositories.user import user_repo

All_REPOS = [student_repo, user_repo]

def reset_all() -> None:
    for repo in All_REPOS:
        repo.reset()