from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


# Exercise (id, nanme, category, equipment_needed(bool))

# Workout (id, date, duration_minutes, notes)

# WorkoutExercises (id, workout_id, exercise_id, reps, sets, duration_seconds)