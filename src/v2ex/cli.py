from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from v2ex import client, display  # noqa: E402

app = typer.Typer(help="V2EX CLI client", no_args_is_help=True)


@app.command()
def hot():
    """Show hot/trending topics."""
    topics = client.hot_topics()
    display.print_topics(topics, title="Hot Topics")


@app.command()
def latest():
    """Show latest topics."""
    topics = client.latest_topics()
    display.print_topics(topics, title="Latest Topics")


@app.command()
def node(
    name: Annotated[str, typer.Argument(help="Node name, e.g. python, programmer")],
    page: Annotated[int, typer.Option("--page", "-p", help="Page number")] = 1,
    info: Annotated[bool, typer.Option("--info", "-i", help="Show node info only")] = False,
):
    """Browse topics in a node."""
    if info:
        n = client.node_info(name)
        display.print_node(n)
        return
    topics = client.node_topics(name, page=page)
    display.print_topics(topics, title=f"Node: {name} (p{page})")


@app.command()
def topic(
    topic_id: Annotated[int, typer.Argument(help="Topic ID")],
    page: Annotated[int, typer.Option("--page", "-p", help="Replies page")] = 1,
):
    """Show topic detail with replies."""
    t = client.topic_detail(topic_id)
    replies = client.topic_replies(topic_id, page=page)
    display.print_topic_detail(t, replies)


@app.command(name="notif")
def notifications(
    page: Annotated[int, typer.Option("--page", "-p", help="Page number")] = 1,
):
    """Show notifications."""
    notifs = client.notifications(page=page)
    display.print_notifications(notifs)


@app.command()
def token():
    """Show current API token info."""
    t = client.token_info()
    display.print_token(t)


@app.command()
def me():
    """Show current authenticated member info."""
    m = client.member_info()
    display.print_member(m)
