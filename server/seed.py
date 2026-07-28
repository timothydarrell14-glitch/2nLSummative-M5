#!/usr/bin/env python3

from datetime import date

from app import app
from models import *

with app.app_context():
    # Reset data in foreign-key order.
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Add exercises.
    squat = Exercise(
        name="Barbell Squat", category="Strength", equipment_needed=True
    )
    bench_press = Exercise(
        name="Bench Press", category="Strength", equipment_needed=True
    )
    push_up = Exercise(name="Push Up", category="Bodyweight", equipment_needed=False)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)

    # Add workout sessions.
    strength_day = Workout(
        date=date(2026, 7, 20),
        duration_minutes=50,
        notes="Lower and upper body strength session.",
    )
    bodyweight_day = Workout(
        date=date(2026, 7, 22),
        duration_minutes=30,
        notes="Quick bodyweight workout.",
    )

    # Connect exercises to workouts with the work performed.
    workout_exercises = [
        WorkoutExercise(
            workout=strength_day,
            exercise=squat,
            reps=10,
            sets=3,
            duration_seconds=0,
        ),
        WorkoutExercise(
            workout=strength_day,
            exercise=bench_press,
            reps=8,
            sets=3,
            duration_seconds=0,
        ),
        WorkoutExercise(
            workout=bodyweight_day,
            exercise=push_up,
            reps=12,
            sets=3,
            duration_seconds=0,
        ),
        WorkoutExercise(
            workout=bodyweight_day,
            exercise=plank,
            reps=1,
            sets=3,
            duration_seconds=180,
        ),
    ]

    db.session.add_all(
        [squat, bench_press, push_up, plank, strength_day, bodyweight_day]
        + workout_exercises
    )
    db.session.commit()
    print("Database seeded successfully.")
