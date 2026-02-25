from __future__ import annotations

import os

import httpx

from v2ex.models import Member, Node, Notification, Reply, Token, Topic

V2_BASE = "https://www.v2ex.com/api/v2"
V1_BASE = "https://www.v2ex.com/api"


def _token() -> str:
    token = os.environ.get("V2EX_TOKEN", "")
    if not token:
        raise SystemExit("V2EX_TOKEN not set. Export it or put it in .env")
    return token


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_token()}"}


def _get(url: str, *, auth: bool = True, params: dict | None = None) -> dict | list:
    headers = _headers() if auth else {}
    resp = httpx.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def _unwrap(data: dict | list) -> list | dict:
    """Unwrap V2 API response envelope."""
    if isinstance(data, dict) and "result" in data:
        return data["result"]
    return data


# --- V1 public endpoints ---


def hot_topics() -> list[Topic]:
    data = _get(f"{V1_BASE}/topics/hot.json", auth=False)
    return [Topic.from_dict(d) for d in data]


def latest_topics() -> list[Topic]:
    data = _get(f"{V1_BASE}/topics/latest.json", auth=False)
    return [Topic.from_dict(d) for d in data]


# --- V2 authenticated endpoints ---


def node_info(name: str) -> Node:
    data = _get(f"{V2_BASE}/nodes/{name}")
    return Node.from_dict(_unwrap(data))


def node_topics(name: str, page: int = 1) -> list[Topic]:
    data = _get(f"{V2_BASE}/nodes/{name}/topics", params={"p": page})
    return [Topic.from_dict(d) for d in _unwrap(data)]


def topic_detail(topic_id: int) -> Topic:
    data = _get(f"{V2_BASE}/topics/{topic_id}")
    return Topic.from_dict(_unwrap(data))


def topic_replies(topic_id: int, page: int = 1) -> list[Reply]:
    data = _get(f"{V2_BASE}/topics/{topic_id}/replies", params={"p": page})
    return [Reply.from_dict(d) for d in _unwrap(data)]


def notifications(page: int = 1) -> list[Notification]:
    data = _get(f"{V2_BASE}/notifications", params={"p": page})
    return [Notification.from_dict(d) for d in _unwrap(data)]


def delete_notification(notification_id: int) -> None:
    resp = httpx.delete(
        f"{V2_BASE}/notifications/{notification_id}",
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()


def token_info() -> Token:
    data = _get(f"{V2_BASE}/token")
    return Token.from_dict(_unwrap(data))


def member_info() -> Member:
    data = _get(f"{V2_BASE}/member")
    return Member.from_dict(_unwrap(data))
