# Workout Tracker API

## Project Description

Workout Tracker is a Flask REST API for recording workouts, maintaining an
exercise library, and recording the exercises performed during each workout.
It uses SQLite, SQLAlchemy, Flask-Migrate, Pipenv, and Marshmallow for data
validation and JSON serialization.

## Installation

From the project root, install the server dependencies and prepare the
database:

```bash
cd server
pipenv install
pipenv run flask --app app db upgrade
pipenv run python seed.py
```

`seed.py` clears existing workout data and replaces it with sample records.

## Run Instructions

Start the development server from the `server` directory:

```bash
pipenv run flask --app app run --port 5555 --debug
```

The API is then available at `http://127.0.0.1:5555`.

## API Endpoints

- `GET /workouts` — Return all workouts, newest first, including their
  recorded exercises.
- `GET /workouts/<id>` — Return one workout by its id.
- `POST /workouts` — Create a workout. JSON fields: `date`,
  `duration_minutes`, and optional `notes`.
- `DELETE /workouts/<id>` — Delete a workout and its associated
  workout-exercise records.
- `GET /exercises` — Return every exercise in the exercise library.
- `GET /exercises/<id>` — Return one exercise by its id.
- `POST /exercises` — Create an exercise. JSON fields: `name`, `category`,
  and `equipment_needed`.
- `DELETE /exercises/<id>` — Delete an exercise and its associated
  workout-exercise records.
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` —
  Add an existing exercise to an existing workout. JSON fields: `reps`,
  `sets`, and `duration_seconds`.

All POST endpoints expect JSON and return validation errors as JSON when the
submitted data is invalid.
