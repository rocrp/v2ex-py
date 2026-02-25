from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Scope(StrEnum):
    EVERYTHING = "everything"
    REGULAR = "regular"


@dataclass(slots=True)
class Member:
    id: int
    username: str
    bio: str = ""
    website: str = ""
    github: str = ""
    url: str = ""
    avatar: str = ""
    avatar_mini: str = ""
    avatar_normal: str = ""
    avatar_large: str = ""
    created: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> Member:
        return cls(
            id=d.get("id", 0),
            username=d.get("username", ""),
            bio=d.get("bio", ""),
            website=d.get("website", ""),
            github=d.get("github", ""),
            url=d.get("url", ""),
            avatar=d.get("avatar", ""),
            avatar_mini=d.get("avatar_mini", ""),
            avatar_normal=d.get("avatar_normal", ""),
            avatar_large=d.get("avatar_large", ""),
            created=d.get("created", 0),
        )


@dataclass(slots=True)
class Node:
    id: int
    name: str
    title: str
    url: str = ""
    header: str = ""
    footer: str = ""
    avatar: str = ""
    topics: int = 0
    created: int = 0
    last_modified: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> Node:
        return cls(
            id=d.get("id", 0),
            name=d.get("name", ""),
            title=d.get("title", ""),
            url=d.get("url", ""),
            header=d.get("header", ""),
            footer=d.get("footer", ""),
            avatar=d.get("avatar", ""),
            topics=d.get("topics", 0),
            created=d.get("created", 0),
            last_modified=d.get("last_modified", 0),
        )


@dataclass(slots=True)
class Topic:
    id: int
    title: str
    content: str = ""
    content_rendered: str = ""
    url: str = ""
    replies: int = 0
    last_reply_by: str = ""
    created: int = 0
    last_modified: int = 0
    last_touched: int = 0
    member: Member | None = None
    node: Node | None = None

    @classmethod
    def from_dict(cls, d: dict) -> Topic:
        member = Member.from_dict(d["member"]) if d.get("member") else None
        node = Node.from_dict(d["node"]) if d.get("node") else None
        return cls(
            id=d.get("id", 0),
            title=d.get("title", ""),
            content=d.get("content", ""),
            content_rendered=d.get("content_rendered", ""),
            url=d.get("url", ""),
            replies=d.get("replies", 0),
            last_reply_by=d.get("last_reply_by", ""),
            created=d.get("created", 0),
            last_modified=d.get("last_modified", 0),
            last_touched=d.get("last_touched", 0),
            member=member,
            node=node,
        )


@dataclass(slots=True)
class Reply:
    id: int
    content: str = ""
    content_rendered: str = ""
    created: int = 0
    member: Member | None = None

    @classmethod
    def from_dict(cls, d: dict) -> Reply:
        member = Member.from_dict(d["member"]) if d.get("member") else None
        return cls(
            id=d.get("id", 0),
            content=d.get("content", ""),
            content_rendered=d.get("content_rendered", ""),
            created=d.get("created", 0),
            member=member,
        )


@dataclass(slots=True)
class Token:
    token: str
    scope: Scope
    expiration: int = 0
    good_for_days: int = 0
    total_used: int = 0
    last_used: int = 0
    created: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> Token:
        return cls(
            token=d.get("token", ""),
            scope=Scope(d.get("scope", "regular")),
            expiration=d.get("expiration", 0),
            good_for_days=d.get("good_for_days", 0),
            total_used=d.get("total_used", 0),
            last_used=d.get("last_used", 0),
            created=d.get("created", 0),
        )


@dataclass(slots=True)
class Notification:
    id: int
    member_id: int = 0
    for_member_id: int = 0
    text: str = ""
    payload: str = ""
    payload_rendered: str = ""
    created: int = 0
    member: Member | None = None

    @classmethod
    def from_dict(cls, d: dict) -> Notification:
        member_data = d.get("member")
        member = None
        if member_data:
            if isinstance(member_data, dict):
                member = Member.from_dict(member_data)
        return cls(
            id=d.get("id", 0),
            member_id=d.get("member_id", 0),
            for_member_id=d.get("for_member_id", 0),
            text=d.get("text", ""),
            payload=d.get("payload", ""),
            payload_rendered=d.get("payload_rendered", ""),
            created=d.get("created", 0),
            member=member,
        )
