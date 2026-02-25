from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from v2ex import client, display  # noqa: E402
from v2ex.models import OutputFormat  # noqa: E402

app = typer.Typer(help="V2EX CLI client", no_args_is_help=True)

_fmt: OutputFormat = OutputFormat.RICH


@app.callback()
def _main(
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
    markdown: Annotated[
        bool, typer.Option("--markdown", "--md", help="Output as Markdown")
    ] = False,
) -> None:
    global _fmt
    if json_output:
        _fmt = OutputFormat.JSON
    elif markdown:
        _fmt = OutputFormat.MARKDOWN


@app.command()
def hot():
    """Show hot/trending topics."""
    topics = client.hot_topics()
    display.output(
        topics,
        _fmt,
        rich_fn=display.print_topics,
        md_fn=display.md_topics,
        rich_kwargs={"title": "Hot Topics"},
        md_kwargs={"title": "Hot Topics"},
    )


@app.command()
def latest():
    """Show latest topics."""
    topics = client.latest_topics()
    display.output(
        topics,
        _fmt,
        rich_fn=display.print_topics,
        md_fn=display.md_topics,
        rich_kwargs={"title": "Latest Topics"},
        md_kwargs={"title": "Latest Topics"},
    )


@app.command()
def node(
    name: Annotated[str, typer.Argument(help="Node name, e.g. python, programmer")],
    page: Annotated[int, typer.Option("--page", "-p", help="Page number")] = 1,
    info: Annotated[bool, typer.Option("--info", "-i", help="Show node info only")] = False,
):
    """Browse topics in a node."""
    if info:
        n = client.node_info(name)
        display.output(
            n,
            _fmt,
            rich_fn=display.print_node,
            md_fn=display.md_node,
        )
        return
    topics = client.node_topics(name, page=page)
    title = f"Node: {name} (p{page})"
    display.output(
        topics,
        _fmt,
        rich_fn=display.print_topics,
        md_fn=display.md_topics,
        rich_kwargs={"title": title},
        md_kwargs={"title": title},
    )


@app.command()
def topic(
    topic_id: Annotated[int, typer.Argument(help="Topic ID")],
    page: Annotated[int, typer.Option("--page", "-p", help="Replies page")] = 1,
):
    """Show topic detail with replies."""
    t = client.topic_detail(topic_id)
    replies = client.topic_replies(topic_id, page=page)
    if _fmt == OutputFormat.JSON:
        import json

        data = {"topic": asdict(t), "replies": [asdict(r) for r in replies]}
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif _fmt == OutputFormat.MARKDOWN:
        print(display.md_topic_detail(t, replies))
    else:
        display.print_topic_detail(t, replies)


@app.command(name="notif")
def notifications(
    page: Annotated[int, typer.Option("--page", "-p", help="Page number")] = 1,
):
    """Show notifications."""
    notifs = client.notifications(page=page)
    display.output(
        notifs,
        _fmt,
        rich_fn=display.print_notifications,
        md_fn=display.md_notifications,
    )


@app.command()
def token():
    """Show current API token info."""
    t = client.token_info()
    display.output(
        t,
        _fmt,
        rich_fn=display.print_token,
        md_fn=display.md_token,
    )


@app.command()
def me():
    """Show current authenticated member info."""
    m = client.member_info()
    display.output(
        m,
        _fmt,
        rich_fn=display.print_member,
        md_fn=display.md_member,
    )
