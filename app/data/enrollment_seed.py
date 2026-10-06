from datetime import date

SEED_ENROLLMENT : list[dict] = [
    {"id" : 1, "student_id" : 1, "course_id" : 1, "start_date" : date(2026, 1, 12), "end_date" : date(2026, 6, 30), "status" : "completed"},
    {"id" : 2, "student_id" : 2, "course_id" : 2, "start_date" : date(2026, 7, 6), "end_date" : None, "status" : "active"},
    {"id" : 3, "student_id" : 3, "course_id" : 3, "start_date" : date(2026, 7, 6), "end_date" : None, "status" : "active"},
    {"id" : 4, "student_id" : 1, "course_id" : 2, "start_date" : date(2026, 7, 6), "end_date" : date(2026, 8, 14), "status" : "dropped"},
    {"id" : 5, "student_id" : 2, "course_id" : 1, "start_date" : date(2026, 11, 2), "end_date" : None, "status" : "pending"},
    {"id" : 6, "student_id" : 3, "course_id" : 1, "start_date" : date(2026, 1, 12), "end_date" : date(2026, 6, 30), "status" : "completed"},
]
