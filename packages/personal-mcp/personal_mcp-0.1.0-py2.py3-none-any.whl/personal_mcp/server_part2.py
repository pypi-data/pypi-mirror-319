                            INSERT INTO entry_tags (entry_id, tag_id)
                            VALUES (?, ?)
                        """, (entry_id, tag_id))
                
                return f"Added {entry.entry_type} journal entry for {entry.date}"

        @self.mcp.tool(description="Analyze journal entries")
        def analyze_journal_entries(
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            entry_type: Optional[str] = None,
            tags: Optional[List[str]] = None
        ) -> Dict:
            """Analyze journal entries and extract insights."""
            with self.db.get_connection() as conn:
                query = """
                    SELECT j.*, GROUP_CONCAT(t.name) as tags
                    FROM journal_entries j
                    LEFT JOIN entry_tags et ON j.id = et.entry_id
                    LEFT JOIN tags t ON et.tag_id = t.id
                    WHERE 1=1
                """
                params = []
                
                if start_date:
                    query += " AND j.date >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND j.date <= ?"
                    params.append(end_date)
                if entry_type:
                    query += " AND j.entry_type = ?"
                    params.append(entry_type)
                
                query += " GROUP BY j.id"
                
                df = pd.read_sql_query(query, conn, params=params)
                
                if df.empty:
                    return {"message": "No entries found for the specified criteria"}
                
                # Filter by tags if specified
                if tags:
                    df = df[df['tags'].apply(lambda x: x and any(tag in x.split(',') for tag in tags))]
                
                metrics = {
                    "entry_count": len(df),
                    "average_metrics": {
                        "mood": round(df['mood'].mean(), 2),
                        "energy": round(df['energy'].mean(), 2),
                        "sleep_quality": round(df['sleep_quality'].mean(), 2),
                        "stress_level": round(df['stress_level'].mean(), 2)
                    },
                    "trends": {
                        "mood_trend": "improving" if df['mood'].is_monotonic_increasing else "varying",
                        "energy_trend": "improving" if df['energy'].is_monotonic_increasing else "varying"
                    }
                }
                
                return metrics

    def setup_resources(self):
        @self.mcp.resource("health://workout-history/{start_date}/{end_date}")
        def get_workout_history(start_date: str, end_date: str) -> str:
            """Get workout history within a date range."""
            with self.db.get_connection() as conn:
                query = """
                    SELECT w.*, e.name as exercise_name, 
                           s.weight, s.reps, s.rpe, s.notes as set_notes
                    FROM workouts w
                    JOIN exercises e ON w.id = e.workout_id
                    JOIN sets s ON e.id = s.exercise_id
                    WHERE w.date BETWEEN ? AND ?
                """
                df = pd.read_sql_query(query, conn, params=(start_date, end_date))
                return df.to_json(orient='records')

        @self.mcp.resource("health://nutrition/{start_date}/{end_date}")
        def get_nutrition_log(start_date: str, end_date: str) -> str:
            """Get nutrition log within a date range."""
            with self.db.get_connection() as conn:
                query = """
                    SELECT m.*, f.name as food_name, 
                           f.amount, f.unit, f.protein, f.calories
                    FROM meals m
                    JOIN foods f ON m.id = f.meal_id
                    WHERE m.date BETWEEN ? AND ?
                """
                df = pd.read_sql_query(query, conn, params=(start_date, end_date))
                return df.to_json(orient='records')

        @self.mcp.resource("journal://entries/{start_date}/{end_date}")
        def get_journal_entries(start_date: str, end_date: str) -> str:
            """Get journal entries within a date range."""
            with self.db.get_connection() as conn:
                query = """
                    SELECT j.*, GROUP_CONCAT(t.name) as tags
                    FROM journal_entries j
                    LEFT JOIN entry_tags et ON j.id = et.entry_id
                    LEFT JOIN tags t ON et.tag_id = t.id
                    WHERE j.date BETWEEN ? AND ?
                    GROUP BY j.id
                """
                df = pd.read_sql_query(query, conn, params=(start_date, end_date))
                return df.to_json(orient='records')

    def setup_prompts(self):
        @self.mcp.prompt()
        def analyze_workout_load(workout_history: str) -> List[Dict]:
            """Analyze workout load and suggest adjustments."""
            return [{
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Please analyze my recent workout history and suggest adjustments based on:
                    1. Shoulder rehabilitation status
                    2. Recent performance
                    3. Recovery patterns
                    4. Energy levels and mood from journal entries
                    
                    Workout History:
                    {workout_history}
                    
                    Particularly focus on:
                    - Safe progression for shoulder exercises
                    - Maintaining leg strength (squats, deadlifts)
                    - Overall volume management
                    - Correlation between workout intensity and recovery metrics"""
                }
            }]

        @self.mcp.prompt()
        def nutrition_recommendations(
            nutrition_log: str, 
            start_date: str, 
            end_date: str
        ) -> List[Dict]:
            """Get personalized nutrition recommendations."""
            return [{
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Based on my meal logs for period {start_date} to {end_date}, please provide:
                    
                    Nutrition Log:
                    {nutrition_log}
                    
                    1. Protein intake optimization
                    2. Meal timing suggestions
                    3. Pre/post workout nutrition
                    4. Supplement timing (creatine, vitamins, omega-3)
                    5. Patterns between nutrition and energy/mood
                    6. Hunger and satisfaction patterns"""
                }
            }]

        @self.mcp.prompt()
        def journal_insights(entries: str) -> List[Dict]:
            """Generate insights from journal entries."""
            return [{
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Please analyze my journal entries and provide insights on:
                    
                    Entries:
                    {entries}
                    
                    1. Patterns in mood and energy levels
                    2. Sleep quality trends and correlations
                    3. Stress management effectiveness
                    4. Relationship between workouts and well-being
                    5. Impact of nutrition on daily metrics
                    6. Progress towards goals mentioned in entries
                    7. Suggestions for improvement based on patterns"""
                }
            }]

    def run(self):
        """Run the MCP server."""
        self.mcp.run()