from datetime import date

from app.domain.course.model import CourseStatus


SEED_COURSE: list[dict] = [
    {
        "id": 1,
        "name": "Web Developer",
        "status": CourseStatus.ACTIVE,
        "teacher_id": 3,
        "start_date": date(2026, 1, 12),
        "end_date": None,
        "description": "Web development fundamentals",
        "classroom": "101",
    },
    {
        "id": 2,
        "name": "Python Developer",
        "status": CourseStatus.ACTIVE,
        "teacher_id": 1,
        "start_date": date(2026, 1, 12),
        "end_date": None,
        "description": "Python programming",
        "classroom": "102",
    },
    {
        "id": 3,
        "name": "UX/UI Designer",
        "status": CourseStatus.PENDING,
        "teacher_id": 4,
        "start_date": date(2026, 7, 6),
        "end_date": None,
        "description": "User experience and interface design",
        "classroom": "103",
    },
]
