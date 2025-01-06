"""Compare haiku generation across different providers."""

import os
import asyncio
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.style import Style
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any, List

from send_2_llm import (
    LLMRequest,
    ProviderType,
    StrategyType,
    LLMManager,
    ProviderInfo,
    LLMResponse
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d, "message": "%(message)s"}'
)

logger = logging.getLogger(__name__)
console = Console()

# Store results for dashboard
results: Dict[str, Dict[str, Any]] = {}

def datetime_handler(obj):
    """Handle datetime serialization to JSON."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def display_dashboard():
    """Display summary dashboard of all provider results."""
    console.print("\n[bold cyan]🌸 Haiku Generation Comparison Dashboard 🌸[/bold cyan]\n")
    
    # Display haikus first
    console.print("[bold magenta]Generated Haikus[/bold magenta]")
    for provider, data in results.items():
        if data.get("status") == "SUCCESS":
            style = "green"
            haiku = data.get("haiku", "No haiku generated")
        elif data.get("status") == "ERROR":
            style = "red"
            haiku = f"Error: {data.get('error', 'Unknown error')}"
        elif data.get("status") == "TIMEOUT":
            style = "yellow"
            haiku = "Timeout: Request took too long"
        else:
            style = "yellow"
            haiku = "Skipped: API key not set"
            
        console.print(Panel(
            haiku,
            title=f"[{style}]{provider}[/{style}]",
            border_style=style,
            padding=(1, 2)
        ))
    
    # Create performance table
    console.print("\n[bold magenta]Performance Metrics[/bold magenta]")
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        padding=(0, 1)
    )
    
    # Add columns
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Model", no_wrap=True)
    table.add_column("Tokens", justify="right")
    table.add_column("Cost ($)", justify="right")
    table.add_column("Latency (s)", justify="right")
    
    # Add rows
    for provider, data in results.items():
        status = data.get("status", "UNKNOWN")
        status_style = {
            "SUCCESS": "[green]✓[/green]",
            "ERROR": "[red]✗[/red]",
            "SKIPPED": "[yellow]⚠[/yellow]",
            "TIMEOUT": "[red]⏱[/red]",
        }.get(status, "[white]?[/white]")
        
        table.add_row(
            provider,
            status_style,
            str(data.get("model", "N/A")),
            str(data.get("total_tokens", "-")),
            f"{data.get('cost', 0.0):.4f}",
            f"{data.get('latency', 0.0):.2f}"
        )
    
    console.print(table)
    
    # Calculate statistics
    success_count = sum(1 for d in results.values() if d.get("status") == "SUCCESS")
    error_count = sum(1 for d in results.values() if d.get("status") == "ERROR")
    skipped_count = sum(1 for d in results.values() if d.get("status") == "SKIPPED")
    timeout_count = sum(1 for d in results.values() if d.get("status") == "TIMEOUT")
    
    total_tokens = sum(d.get("total_tokens", 0) for d in results.values())
    total_cost = sum(d.get("cost", 0.0) for d in results.values())
    avg_latency = sum(d.get("latency", 0.0) for d in results.values() if d.get("latency")) / success_count if success_count else 0
    
    # Display summary statistics
    console.print("\n[bold magenta]Summary Statistics[/bold magenta]")
    stats_table = Table.grid(padding=1, expand=True)
    stats_table.add_column(style="bold cyan", justify="right")
    stats_table.add_column(justify="left")
    stats_table.add_column(style="bold cyan", justify="right")
    stats_table.add_column(justify="left")
    
    stats_table.add_row(
        "Total Providers:", str(len(results)),
        "Success Rate:", f"[green]{success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)[/green]"
    )
    stats_table.add_row(
        "Successful:", f"[green]{success_count}[/green]",
        "Failed:", f"[red]{error_count}[/red]"
    )
    stats_table.add_row(
        "Skipped:", f"[yellow]{skipped_count}[/yellow]",
        "Timeouts:", f"[red]{timeout_count}[/red]"
    )
    stats_table.add_row(
        "Total Tokens:", str(total_tokens),
        "Avg Latency:", f"{avg_latency:.2f}s"
    )
    stats_table.add_row(
        "Total Cost:", f"${total_cost:.4f}",
        "Avg Cost/Request:", f"${(total_cost/success_count if success_count else 0):.4f}"
    )
    
    console.print(Panel(stats_table, border_style="cyan", padding=(1, 2)))
    
    # Print conclusion
    conclusion = ""
    if success_count == len(results):
        conclusion = "[green]All providers successfully generated haikus![/green]"
    elif success_count == 0:
        conclusion = "[red]No providers were able to generate haikus.[/red]"
    else:
        conclusion = f"[yellow]{success_count} out of {len(results)} providers successfully generated haikus.[/yellow]"
    
    console.print("\n[bold magenta]Conclusion[/bold magenta]")
    console.print(Panel(conclusion, border_style="magenta", padding=(1, 2)))

async def generate_haiku(llm: LLMManager, provider: ProviderInfo) -> None:
    """Generate haiku using specified provider."""
    start_time = datetime.now()
    provider_name = provider.type.value
    
    try:
        # Check if provider's API key is set
        env_var = f"{provider_name.upper()}_API_KEY"
        if not os.getenv(env_var):
            console.print(f"[yellow]Skipping {provider_name} - {env_var} not set[/yellow]")
            results[provider_name] = {
                "status": "SKIPPED",
                "error": f"{env_var} not set",
                "haiku": "API key not set"
            }
            return

        # Create request
        request = LLMRequest(
            prompt="Generate a haiku about cherry blossoms",
            provider_type=provider.type,
            strategy=StrategyType.SINGLE,
            temperature=0.4,
            system_prompt_type="haiku"
        )
        
        # Display provider info
        console.print(f"\n[cyan]Trying {provider_name}...[/cyan]")
        
        # Generate haiku with timeout
        try:
            async with asyncio.timeout(60):  # 60 second timeout
                logger.debug(f"Starting request to {provider_name}")
                response = await llm.generate(request)
                logger.debug(f"Got response from {provider_name}")
                
                # Store results
                end_time = datetime.now()
                latency = (end_time - start_time).total_seconds()
                
                results[provider_name] = {
                    "status": "SUCCESS",
                    "model": response.metadata.model,
                    "total_tokens": response.metadata.usage.total_tokens,
                    "cost": response.metadata.usage.cost or 0.0,
                    "latency": latency,
                    "haiku": response.text
                }
                
                # Display result
                console.print(Panel(response.text, title=f"Haiku from {provider_name}"))
                
                # Display metadata
                metadata_json = json.dumps(response.metadata.model_dump(), indent=2, default=datetime_handler)
                console.print(Syntax(metadata_json, "json", theme="monokai", line_numbers=True))
                
        except asyncio.TimeoutError:
            results[provider_name] = {
                "status": "TIMEOUT",
                "error": "Request timed out after 60s",
                "haiku": "Timeout occurred"
            }
            console.print(f"[red]Timeout error with {provider_name}[/red]")
            
    except Exception as e:
        logger.exception(f"Error with {provider_name}")
        results[provider_name] = {
            "status": "ERROR",
            "error": str(e),
            "haiku": f"Error: {str(e)}"
        }
        console.print(f"[red]Error with {provider_name}: {str(e)}[/red]")

async def main():
    """Run the example."""
    try:
        # Initialize LLM manager
        logger.info("Initializing LLM manager")
        llm = LLMManager()
        
        # Get available providers
        logger.info("Getting available providers")
        providers = llm.get_available_providers()
        logger.info(f"Found {len(providers)} providers")
        
        # Display available providers
        table = Table(title="Available Providers")
        table.add_column("Provider")
        table.add_column("Priority")
        table.add_column("Fallback")
        table.add_column("Description")
        
        for provider in providers:
            logger.debug(f"Adding provider to table: {provider.type.value}")
            table.add_row(
                provider.type.value,
                str(provider.priority),
                "✓" if provider.is_fallback else "✗",
                provider.description
            )
        
        console.print(table)
        console.print()
        
        # Generate haiku with each provider
        for provider in providers:
            logger.info(f"Processing provider: {provider.type.value}")
            await generate_haiku(llm, provider)
            
        # Display final dashboard
        display_dashboard()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        logger.exception("Unexpected error")
        console.print(f"[red]Unexpected error: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
        # Still show dashboard with partial results
        display_dashboard()
    except Exception as e:
        logger.exception("Fatal error")
        console.print(f"[red]Fatal error: {str(e)}[/red]") 