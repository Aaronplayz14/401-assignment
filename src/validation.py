import re
from datetime import datetime



ISO_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)


def validate_published(value: str) -> bool:

    if not ISO_UTC_PATTERN.fullmatch(value):
        return False

    try:
        datetime.fromisoformat(
            value[:-1] + "+00:00"
        )
    except ValueError:
        return False

    return True


def validate_item_values(data: dict):
    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            raise ValueError("title must be a non-empty string")

    if "source" in data:
        source = data["source"]

        if source is None:
            raise ValueError("source must not be null")

        if not isinstance(source, dict):
            raise ValueError("source must be an object")

        name = source.get("name")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("source.name must be a non-empty string")

    if "publishedAt" in data:
        value = data["publishedAt"]

        if value is None:
            raise ValueError("publishedAt must be a string")

        if not validate_published(value):
            raise ValueError(
                "publishedAt must be a valid UTC ISO 8601 datetime ending in Z"
            )

    if "url" in data:
        if not isinstance(data["url"], str) or not data["url"].strip():
            raise ValueError("url must be a non-empty string")

    if "summary" in data:
        if not isinstance(data["summary"], str):
            raise ValueError("summary must be a string")

    if "tags" in data:
        tags = data["tags"]

        if not isinstance(tags, list):
            raise ValueError("tags must be an array of strings")

        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError("tags must be an array of strings")