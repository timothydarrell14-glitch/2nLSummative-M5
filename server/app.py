from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas.exerciseSchema import ExerciseSchema
from schemas.workoutSchema import WorkoutExerciseSchema, WorkoutSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def validation_error_response(error):
    return jsonify({"errors": error.messages}), 400


def json_body():
    body = request.get_json(silent=True)
    if body is None:
        return None, (jsonify({"errors": {"json": ["A JSON body is required."]}}), 400)
    return body, None


def not_found_response(resource):
    return jsonify({"error": f"{resource} not found."}), 404


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc(), Workout.id.desc()).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return not_found_response("Workout")
    return jsonify(workout_schema.dump(workout)), 200


@app.post("/workouts")
def create_workout():
    body, error = json_body()
    if error:
        return error

    try:
        workout_data = workout_schema.load(body)
    except ValidationError as error:
        return validation_error_response(error)

    workout = Workout(**workout_data)
    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_schema.dump(workout)), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return not_found_response("Workout")

    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return not_found_response("Exercise")
    return jsonify(exercise_schema.dump(exercise)), 200


@app.post("/exercises")
def create_exercise():
    body, error = json_body()
    if error:
        return error

    try:
        exercise_data = exercise_schema.load(body)
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as error:
        return validation_error_response(error)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": {"name": ["Exercise name must be unique."]}}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return not_found_response("Exercise")

    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def create_workout_exercise(workout_id, exercise_id):
    if db.session.get(Workout, workout_id) is None:
        return not_found_response("Workout")
    if db.session.get(Exercise, exercise_id) is None:
        return not_found_response("Exercise")

    body, error = json_body()
    if error:
        return error

    try:
        workout_exercise_data = workout_exercise_schema.load(
            {**body, "workout_id": workout_id, "exercise_id": exercise_id}
        )
    except ValidationError as error:
        return validation_error_response(error)

    try:
        workout_exercise = WorkoutExercise(**workout_exercise_data)
        db.session.add(workout_exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {"errors": {"workout_exercise": ["Could not save workout exercise."]}}
        ), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
