# run_scenarios.py
import asyncio, os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

from backend.client.scenarios import Scenario, ScenarioResult, scenarios_list

load_dotenv()
MCP_HOST_URL = os.getenv("MCP_HOST_URL")
LLM_MODEL    = os.getenv("LLM_MODEL")

console = Console()
console.print(f"⤷ using MCP host: [bold cyan]{MCP_HOST_URL}[/]\n")

# ——— Agents ——————————————————————————————————————————
mcp_agent = Agent(
    model=LLM_MODEL,
    mcp_servers=[MCPServerHTTP(url=MCP_HOST_URL)],
)

# ——— Runner ——————————————————————————————————————————

async def run_scenario(s: Scenario):
    """Run one scenario with a live spinner and return the result."""
    with console.status(f"[yellow]Running[/] [bold]{s.name}[/]…", spinner="dots") as status:
        mcp_res = await mcp_agent.run(s.prompt)

    return mcp_res.output

async def main():
    async with mcp_agent.run_mcp_servers():
        for scenario in scenarios_list:
            console.rule(f"[orange] Scenario: {scenario.name}")
            console.print(Panel(scenario.prompt, title="📣 Prompt", style="bright_blue"))

            mcp_res = await run_scenario(scenario)

            console.print(Panel(mcp_res, title="💻 Server", style="bold cyan"))

if __name__ == "__main__":
    asyncio.run(main())
