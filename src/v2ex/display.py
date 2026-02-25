from __future__ import annotations

import html
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Callable

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from v2ex.models import Member, Node, Notification, OutputFormat, Reply, Token, Topic

console = Console()


def _relative_time(ts: int) -> str:
    if ts == 0:
        return ""
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    diff = datetime.now(tz=timezone.utc) - dt
    secs = int(diff.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    mins = secs // 60
    if mins < 60:
        return f"{mins}m ago"
    hours = mins // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    if days < 30:
        return f"{days}d ago"
    return dt.strftime("%Y-%m-%d")


def _strip_html(text: str) -> str:
    text = html.unescape(text)
    return re.sub(r"<[^>]+>", "", text)


def _to_dict(obj: Any) -> Any:
    """Convert dataclass (or list of dataclasses) to plain dicts for JSON."""
    if isinstance(obj, list):
        return [asdict(item) for item in obj]
    return asdict(obj)


# ---------------------------------------------------------------------------
# Rich formatters (existing)
# ---------------------------------------------------------------------------


def print_topics(topics: list[Topic], *, title: str = "Topics") -> None:
    table = Table(title=title, show_lines=False, expand=True)
    table.add_column("#", style="dim", width=8, justify="right")
    table.add_column("Title", ratio=3)
    table.add_column("Node", style="cyan", width=14)
    table.add_column("Author", style="green", width=14)
    table.add_column("Replies", style="yellow", width=7, justify="right")
    table.add_column("Time", style="dim", width=10)

    for t in topics:
        node_name = t.node.title if t.node else ""
        author = t.member.username if t.member else ""
        table.add_row(
            str(t.id),
            t.title,
            node_name,
            author,
            str(t.replies),
            _relative_time(t.created),
        )
    console.print(table)


def print_topic_detail(topic: Topic, replies: list[Reply]) -> None:
    author = topic.member.username if topic.member else "?"
    node_name = topic.node.title if topic.node else ""
    header = f"[bold]{topic.title}[/bold]\n[dim]{author} · {node_name} · {_relative_time(topic.created)} · {topic.replies} replies[/dim]"
    console.print(Panel(header, border_style="blue"))

    if topic.content:
        console.print()
        console.print(Markdown(topic.content))
        console.print()

    if not replies:
        return

    console.print(f"[bold]--- Replies ({len(replies)}) ---[/bold]")
    for i, r in enumerate(replies, 1):
        author = r.member.username if r.member else "?"
        time_str = _relative_time(r.created)
        console.print(f"\n[green]#{i} {author}[/green] [dim]{time_str}[/dim]")
        if r.content:
            console.print(Text(r.content))


def print_notifications(notifications: list[Notification]) -> None:
    if not notifications:
        console.print("[dim]No notifications.[/dim]")
        return

    table = Table(title="Notifications", show_lines=True, expand=True)
    table.add_column("ID", style="dim", width=10, justify="right")
    table.add_column("From", style="green", width=14)
    table.add_column("Content", ratio=3)
    table.add_column("Time", style="dim", width=10)

    for n in notifications:
        who = n.member.username if n.member else str(n.member_id)
        text = _strip_html(n.payload_rendered) if n.payload_rendered else n.text
        table.add_row(str(n.id), who, text, _relative_time(n.created))
    console.print(table)


def print_token(token: Token) -> None:
    masked = token.token[:8] + "..." + token.token[-4:] if len(token.token) > 12 else token.token
    table = Table(title="Token Info", show_lines=False)
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Token", masked)
    table.add_row("Scope", token.scope.value)
    table.add_row("Good for", f"{token.good_for_days} days")
    table.add_row("Total used", str(token.total_used))
    table.add_row("Last used", _relative_time(token.last_used))
    table.add_row("Created", _relative_time(token.created))
    table.add_row("Expiration", _relative_time(token.expiration))
    console.print(table)


def print_member(member: Member) -> None:
    table = Table(title=f"Member: {member.username}", show_lines=False)
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("ID", str(member.id))
    table.add_row("Username", member.username)
    if member.bio:
        table.add_row("Bio", member.bio)
    if member.website:
        table.add_row("Website", member.website)
    if member.github:
        table.add_row("GitHub", member.github)
    table.add_row("Joined", _relative_time(member.created))
    console.print(table)


def print_node(node: Node) -> None:
    table = Table(title=f"Node: {node.title}", show_lines=False)
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Name", node.name)
    table.add_row("Title", node.title)
    table.add_row("Topics", str(node.topics))
    if node.header:
        table.add_row("Header", _strip_html(node.header))
    console.print(table)


# ---------------------------------------------------------------------------
# Markdown formatters
# ---------------------------------------------------------------------------


def md_topics(topics: list[Topic], *, title: str = "Topics") -> str:
    lines = [f"# {title}", "", "| ID | Title | Node | Author | Replies | Time |"]
    lines.append("| ---: | --- | --- | --- | ---: | --- |")
    for t in topics:
        node_name = t.node.title if t.node else ""
        author = t.member.username if t.member else ""
        lines.append(
            f"| {t.id} | {t.title} | {node_name} | {author} | {t.replies} | {_relative_time(t.created)} |"
        )
    return "\n".join(lines)


def md_topic_detail(topic: Topic, replies: list[Reply]) -> str:
    author = topic.member.username if topic.member else "?"
    node_name = topic.node.title if topic.node else ""
    lines = [
        f"# {topic.title}",
        f"*{author} · {node_name} · {_relative_time(topic.created)} · {topic.replies} replies*",
        "",
    ]
    if topic.content:
        lines.append(topic.content)
        lines.append("")
    if replies:
        lines.append(f"## Replies ({len(replies)})")
        lines.append("")
        for i, r in enumerate(replies, 1):
            r_author = r.member.username if r.member else "?"
            lines.append(f"**#{i} {r_author}** *{_relative_time(r.created)}*")
            if r.content:
                lines.append(r.content)
            lines.append("")
    return "\n".join(lines)


def md_notifications(notifications: list[Notification]) -> str:
    if not notifications:
        return "No notifications."
    lines = ["# Notifications", "", "| ID | From | Content | Time |"]
    lines.append("| ---: | --- | --- | --- |")
    for n in notifications:
        who = n.member.username if n.member else str(n.member_id)
        text = _strip_html(n.payload_rendered) if n.payload_rendered else n.text
        # Escape pipes in content for markdown table
        text = text.replace("|", "\\|")
        lines.append(f"| {n.id} | {who} | {text} | {_relative_time(n.created)} |")
    return "\n".join(lines)


def md_token(token: Token) -> str:
    masked = token.token[:8] + "..." + token.token[-4:] if len(token.token) > 12 else token.token
    return "\n".join(
        [
            "# Token Info",
            "",
            f"- **Token**: {masked}",
            f"- **Scope**: {token.scope.value}",
            f"- **Good for**: {token.good_for_days} days",
            f"- **Total used**: {token.total_used}",
            f"- **Last used**: {_relative_time(token.last_used)}",
            f"- **Created**: {_relative_time(token.created)}",
            f"- **Expiration**: {_relative_time(token.expiration)}",
        ]
    )


def md_member(member: Member) -> str:
    lines = [
        f"# Member: {member.username}",
        "",
        f"- **ID**: {member.id}",
        f"- **Username**: {member.username}",
    ]
    if member.bio:
        lines.append(f"- **Bio**: {member.bio}")
    if member.website:
        lines.append(f"- **Website**: {member.website}")
    if member.github:
        lines.append(f"- **GitHub**: {member.github}")
    lines.append(f"- **Joined**: {_relative_time(member.created)}")
    return "\n".join(lines)


def md_node(node: Node) -> str:
    lines = [
        f"# Node: {node.title}",
        "",
        f"- **Name**: {node.name}",
        f"- **Title**: {node.title}",
        f"- **Topics**: {node.topics}",
    ]
    if node.header:
        lines.append(f"- **Header**: {_strip_html(node.header)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output dispatcher
# ---------------------------------------------------------------------------


def output(
    data: Any,
    fmt: OutputFormat,
    *,
    rich_fn: Callable[..., None],
    md_fn: Callable[..., str],
    rich_kwargs: dict[str, Any] | None = None,
    md_kwargs: dict[str, Any] | None = None,
) -> None:
    """Route output to rich table, JSON, or markdown based on format."""
    if fmt == OutputFormat.JSON:
        print(json.dumps(_to_dict(data), ensure_ascii=False, indent=2))
    elif fmt == OutputFormat.MARKDOWN:
        print(md_fn(data, **(md_kwargs or {})))
    else:
        rich_fn(data, **(rich_kwargs or {}))
