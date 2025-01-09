import json
from typing import Optional

from ..models import Workout, ListPrompt


def register_workout_tools(mcp, db):
    """Register workout-related tools."""

    @mcp.tool(description="Log a workout session with exercises")
    def log_workout(workout: Workout) -> str:
        """Log a workout session with exercises and subjective feedback."""
        with db.get_connection() as conn:
            cursor = conn.cursor()

            # Create workout entry
            cursor.execute(
                """
                INSERT INTO workouts (date, perceived_effort, post_workout_feeling, notes)
                VALUES (?, ?, ?, ?)
            """,
                (
                    workout.date,
                    workout.perceived_effort,
                    workout.post_workout_feeling,
                    workout.notes,
                ),
            )
            workout_id = cursor.lastrowid

            # Add exercises and sets
            for exercise in workout.exercises:
                cursor.execute(
                    """
                    INSERT INTO exercises (workout_id, name)
                    VALUES (?, ?)
                """,
                    (workout_id, exercise.name),
                )
                exercise_id = cursor.lastrowid

                for set_data in exercise.sets:
                    cursor.execute(
                        """
                        INSERT INTO sets (exercise_id, weight, reps, rpe, notes)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            exercise_id,
                            set_data.weight,
                            set_data.reps,
                            set_data.rpe,
                            set_data.notes,
                        ),
                    )

            conn.commit()
            return f"Logged workout for {workout.date} with {len(workout.exercises)} exercises"

    @mcp.tool(description="Calculate safe training weights based on recovery")
    def calculate_training_weights(
        exercise: str,
        base_weight: float,
        days_since_surgery: Optional[int] = None,
        recent_pain_level: Optional[int] = None,
        recent_rpe: Optional[float] = None,
    ) -> str:
        """Calculate safe training weights taking into account shoulder recovery."""
        base_reduction = 0.4  # 40% reduction post-surgery
        recovery_factor = min((days_since_surgery or 0) / 180, 1) if days_since_surgery else 1
        pain_reduction = (recent_pain_level or 0) * 0.05 if recent_pain_level else 0

        rpe_adjustment = 0
        if recent_rpe:
            if recent_rpe > 8:  # Too hard
                rpe_adjustment = -0.05
            elif recent_rpe < 6:  # Too easy
                rpe_adjustment = 0.05

        recommended_weight = base_weight * (1 - base_reduction) * (0.6 + 0.4 * recovery_factor)
        recommended_weight *= 1 - pain_reduction
        recommended_weight *= 1 + rpe_adjustment

        result = {
            "recommended_weight": round(recommended_weight, 1),
            "recommended_reps": "12-15 for rehabilitation phase",
            "notes": "Focus on form and controlled movement",
        }

        return json.dumps(result)

    @mcp.tool(description="List workout sessions")
    def list_workouts(params: ListPrompt) -> str:
        """List workout sessions with pagination."""
        with db.get_connection() as conn:
            query = """
                SELECT w.*,
                       e.id as exercise_id, e.name as exercise_name,
                       s.weight, s.reps, s.rpe, s.notes as set_notes
                FROM workouts w
                LEFT JOIN exercises e ON w.id = e.workout_id
                LEFT JOIN sets s ON e.id = s.exercise_id
                ORDER BY w.date DESC
                LIMIT ? OFFSET ?
            """
            
            cursor = conn.cursor()
            cursor.execute(query, [params.limit, params.offset])
            rows = cursor.fetchall()
            
            if not rows:
                return json.dumps({"workouts": []})
            
            workouts = {}
            for row in rows:
                workout_id = row[0]
                if workout_id not in workouts:
                    workouts[workout_id] = {
                        "date": row[1],
                        "perceived_effort": row[2],
                        "post_workout_feeling": row[3],
                        "notes": row[4],
                        "exercises": {}
                    }
                
                if row[5]:  # If there's an exercise
                    exercise_id = row[5]
                    if exercise_id not in workouts[workout_id]["exercises"]:
                        workouts[workout_id]["exercises"][exercise_id] = {
                            "name": row[6],
                            "sets": []
                        }
                    
                    if row[7]:  # If there's a set
                        workouts[workout_id]["exercises"][exercise_id]["sets"].append({
                            "weight": row[7],
                            "reps": row[8],
                            "rpe": row[9],
                            "notes": row[10]
                        })
            
            # Convert exercises dict to list and sort by exercise_id
            for workout in workouts.values():
                workout["exercises"] = list(workout["exercises"].values())
            
            return json.dumps({"workouts": list(workouts.values())})
