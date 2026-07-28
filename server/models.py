from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


# Exercise (id, name, category, equipment_needed(bool))
class Exercise(db.Model):
    """A type of exercise that can be added to a workout."""

    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint("name", name="uq_exercises_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    @validates("name")
    def validate_name(self, value):
        value = value.strip() if isinstance(value, str) else ""
        if len(value) < 2:
            raise ValueError("Exercise name must contain at least 2 characters.")
        return value

    @validates("category")
    def validate_category(self, value):
        value = value.strip() if isinstance(value, str) else ""
        if not value:
            raise ValueError("Exercise category is required.")
        return value


# Workout (id, date, duration_minutes, notes)
class Workout(db.Model):
    """A recorded workout session."""

    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workouts_positive_duration"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    @validates("duration_minutes")
    def validate_duration_minutes(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Workout duration must be a positive whole number of minutes.")
        return value


# WorkoutExercises (id, workout_id, exercise_id, reps, sets, duration_seconds)
class WorkoutExercise(db.Model):
    """An exercise performed during a particular workout."""

    __tablename__ = "workout_exercises"
    __table_args__ = (
        CheckConstraint("reps > 0", name="ck_workout_exercises_positive_reps"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer, nullable=False, default=0)
    sets = db.Column(db.Integer, nullable=False, default=0)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Reps must be a positive whole number.")
        return value
