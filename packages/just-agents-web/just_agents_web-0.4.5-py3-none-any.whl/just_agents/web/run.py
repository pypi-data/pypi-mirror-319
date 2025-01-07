from pathlib import Path
from typing import Optional
from just_agents.web.rest_api import AgentRestAPI
import uvicorn
import typer

app = typer.Typer()

def run_server(
    config: Path,
    host: str = "0.0.0.0",
    port: int = 8088,
    workers: int = 1,
    title: str = "Just-Agent endpoint",
    agent_section: Optional[str] = None,
    agent_parent_section: Optional[str] = None
) -> None:
    """
    Run the FastAPI server with the given configuration.
    
    Args:
        config_path: Path to the YAML configuration file
        host: Host to bind the server to
        port: Port to run the server on
        workers: Number of worker processes
        title: Title for the API endpoint
        agent_section: Optional section name in the config file
        agent_parent_section: Optional parent section name in the config file
    """
    api = AgentRestAPI(
        agent_config=config,
        title=title,
        agent_section=agent_section,
        agent_parent_section=agent_parent_section
    )
    
    uvicorn.run(
        api,
        host=host,
        port=port,
        workers=workers
    )

@app.command()
def run_server_command(
    config: Path = typer.Option(help="Path to the YAML configuration file"), #typer.Argument(..., help="Path to the YAML configuration file"),
    host: str = typer.Option("0.0.0.0", help="Host to bind the server to"),
    port: int = typer.Option(8088, help="Port to run the server on"),
    workers: int = typer.Option(1, help="Number of worker processes"),
    title: str = typer.Option("Just-Agent endpoint", help="Title for the API endpoint"),
    section: Optional[str] = typer.Option(None, help="Optional section name in the config file"),
    parent_section: Optional[str] = typer.Option(None, help="Optional parent section name in the config file")
) -> None:
    """Run the FastAPI server with the given configuration."""
    run_server(
        config=config,
        host=host,
        port=port,
        workers=workers,
        title=title,
        section=section,
        parent_section=parent_section
    )

if __name__ == "__main__":
    app()