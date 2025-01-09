import json
from datetime import datetime
from typing import Optional

from ..models import Meal, ListPrompt


def register_nutrition_tools(mcp, db):
    """Register nutrition-related tools."""

    @mcp.tool(description="Log a meal with nutritional information")
    def log_meal(meal: Meal) -> str:
        """Log a meal with its components and subjective measures."""
        with db.get_connection() as conn:
            cursor = conn.cursor()

            # Calculate totals
            total_protein = sum(food.protein or 0 for food in meal.foods)
            total_calories = sum(food.calories or 0 for food in meal.foods)

            # Create meal entry
            cursor.execute(
                """
                INSERT INTO meals (date, meal_type, time, total_protein, total_calories,
                                 hunger_level, satisfaction_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    meal.date,
                    meal.meal_type,
                    meal.time,
                    total_protein,
                    total_calories,
                    meal.hunger_level,
                    meal.satisfaction_level,
                    meal.notes,
                ),
            )
            meal_id = cursor.lastrowid

            # Add foods
            for food in meal.foods:
                cursor.execute(
                    """
                    INSERT INTO foods (meal_id, name, amount, unit, protein, calories)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (meal_id, food.name, food.amount, food.unit, food.protein, food.calories),
                )

            conn.commit()
            return (
                f"Logged {meal.meal_type} with {total_protein}g protein and "
                f"{total_calories} calories"
            )

    @mcp.tool(description="Check daily nutrition targets")
    def check_nutrition_targets(date: Optional[str] = None) -> str:
        """Check progress towards daily nutrition targets."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT SUM(total_protein), SUM(total_calories),
                       AVG(hunger_level), AVG(satisfaction_level)
                FROM meals
                WHERE date = ?
            """,
                (date,),
            )
            protein, calories, avg_hunger, avg_satisfaction = cursor.fetchone()

            target_protein = 160  # 2g per kg at 80kg body weight
            target_calories = 2500

            result = {
                "date": date,
                "protein": {
                    "current": protein or 0,
                    "target": target_protein,
                    "remaining": max(0, target_protein - (protein or 0)),
                },
                "calories": {
                    "current": calories or 0,
                    "target": target_calories,
                    "remaining": max(0, target_calories - (calories or 0)),
                },
                "metrics": {
                    "average_hunger": round(avg_hunger, 1) if avg_hunger else None,
                    "average_satisfaction": (
                        round(avg_satisfaction, 1) if avg_satisfaction else None
                    ),
                },
            }

            return json.dumps(result)

    @mcp.tool(description="List nutrition entries")
    def list_nutrition_entries(params: ListPrompt) -> str:
        """List nutrition entries with pagination."""
        with db.get_connection() as conn:
            query = """
                SELECT m.*, f.id as food_id, f.name as food_name,
                       f.amount, f.unit, f.protein, f.calories
                FROM meals m
                LEFT JOIN foods f ON m.id = f.meal_id
                ORDER BY m.date DESC, m.time DESC
                LIMIT ? OFFSET ?
            """
            
            cursor = conn.cursor()
            cursor.execute(query, [params.limit, params.offset])
            rows = cursor.fetchall()
            
            if not rows:
                return json.dumps({"meals": []})
            
            meals = {}
            for row in rows:
                meal_id = row[0]
                if meal_id not in meals:
                    meals[meal_id] = {
                        "date": row[1],
                        "meal_type": row[2],
                        "time": row[3],
                        "total_protein": row[4],
                        "total_calories": row[5],
                        "hunger_level": row[6],
                        "satisfaction_level": row[7],
                        "notes": row[8],
                        "foods": []
                    }
                
                if row[9]:  # If there's a food item
                    meals[meal_id]["foods"].append({
                        "name": row[10],
                        "amount": row[11],
                        "unit": row[12],
                        "protein": row[13],
                        "calories": row[14]
                    })
            
            return json.dumps({"meals": list(meals.values())})
