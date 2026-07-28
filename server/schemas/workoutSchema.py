from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate, validates_schema

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

    @validates_schema
    def validate_activity_measurement(self, data, **kwargs):
        """Require a meaningful set-based or timed exercise record."""
        if data["sets"] == 0 and data["duration_seconds"] == 0:
            raise ValidationError(
                "Provide at least one set or a duration in seconds.",
                field_name="sets",
            )


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
