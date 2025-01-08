from mcp.server.fastmcp import FastMCP
from .database import Database
from .tools import register_workout_tools, register_nutrition_tools, register_journal_tools
from .resources import register_resources
from .prompts import register_prompts

class PersonalMCP:
    def __init__(self, name: str = "Personal Assistant", db_path: str = "personal_tracking.db"):
        self.mcp = FastMCP(name)
        self.db = Database(db_path)
        self.setup_tools()
        self.setup_resources()
        self.setup_prompts()

    def setup_tools(self):
        register_workout_tools(self.mcp, self.db)
        register_nutrition_tools(self.mcp, self.db)
        register_journal_tools(self.mcp, self.db)

    def setup_resources(self):
        register_resources(self.mcp, self.db)

    def setup_prompts(self):
        register_prompts(self.mcp)

    def run(self):
        """Run the MCP server."""
        self.mcp.run()