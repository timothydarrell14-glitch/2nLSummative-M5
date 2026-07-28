from marshmallow import EXCLUDE, Schema, fields, validate

from .workoutSchema import WorkoutExerciseSchema


class ExerciseSchema(Schema):
    """Serialize an exercise and the workouts in which it was performed."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    category = fields.String(
        required=True, validate=validate.Length(min=1, max=50)
    )
    equipment_needed = fields.Boolean(required=True)
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, dump_only=True
    )
