from marshmallow import EXCLUDE, Schema, fields, validate, Marshmallow


ma = Marshmallow()

class WorkoutExerciseSchema(Schema):
    """Serialize an exercise recorded as part of a workout."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True, load_only=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(required=True, validate=validate.Range(min=1))
    sets = fields.Integer(required=True, validate=validate.Range(min=0))
    duration_seconds = fields.Integer(required=True, validate=validate.Range(min=0))


class WorkoutSchema(Schema):
    """Serialize a workout and its recorded exercises."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1)
    )
    notes = fields.String(allow_none=True, validate=validate.Length(max=1000))
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True
    )
