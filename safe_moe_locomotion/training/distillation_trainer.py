"""Distillation adapter placeholder."""


def validate_teacher_student(teacher: str, student: str) -> None:
    if teacher == student:
        raise ValueError("teacher and student checkpoints must be different")

