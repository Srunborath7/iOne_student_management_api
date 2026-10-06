from app.repositories.student import student_repo
from app.repositories.user import user_repo
from app.repositories.course import course_repo
from app.repositories.enrollment import enrollment_repo
from app.repositories.teacher import teacher_repo
from app.repositories.score_report import score_report_repo
from app.repositories.attendance import attendance_repo

All_REPOS = [student_repo, user_repo, course_repo, enrollment_repo, teacher_repo, score_report_repo, attendance_repo]

def reset_all() -> None:
    for repo in All_REPOS:
        repo.reset()
