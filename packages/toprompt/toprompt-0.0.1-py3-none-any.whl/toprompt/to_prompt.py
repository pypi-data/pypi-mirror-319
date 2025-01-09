from __future__ import annotations

import argparse
import asyncio
from collections.abc import Callable, Coroutine
from datetime import datetime
import re
from typing import Any, Literal, Protocol, TypeVar

from clinspector import get_cmd_info
from fieldz import get_adapter
from llmling import BasePrompt
from pydantic import BaseModel
from sqlmodel import SQLModel

from toprompt.cli_types import (
    ClickCommandLike,
    TyperCommandLike,
    format_cli_command,
    is_cli_object,
)
from toprompt.dataclass_types import format_dataclass_like
from toprompt.sqlite_types import (
    FileDatabaseLike,
    InMemoryDatabaseLike,
    get_sqlite_schema,
    is_sqlite_db,
)
from toprompt.sqlmodel_types import generate_schema_description


T = TypeVar("T")


class PromptConvertible(Protocol):
    """Protocol for instances that can be converted to prompts."""

    def __prompt__(self) -> str: ...


class PromptTypeConvertible(Protocol):
    """Protocol for types that can be converted to prompts."""

    @classmethod
    def __prompt_type__(cls) -> str: ...


class FieldFormattable(Protocol):
    """Protocol for types that can be formatted through their fields."""

    __annotations__: dict[str, Any]


type AnyPromptType = (
    str
    | PromptConvertible
    | PromptTypeConvertible
    | FieldFormattable
    | BaseModel
    | BasePrompt
    | InMemoryDatabaseLike
    | ClickCommandLike
    | TyperCommandLike
    | argparse.ArgumentParser
    | FileDatabaseLike
    | datetime
    | re.Pattern
    | dict[str, Any]
    | list[Any]
    | tuple[Any, ...]
    | Callable[..., str]
    | Coroutine[Any, Any, str]
)


class Template(str):  # noqa: SLOT000
    """Marker class for strings that should be templated."""


async def to_prompt(  # noqa: PLR0911
    obj: AnyPromptType,
    *,
    template_mode: Literal["off", "explicit", "all"] = "off",
    **kwargs: Any,
) -> str:
    """Convert any supported type to a prompt string.

    Args:
        obj: Object to convert
        template_mode: How to handle templating:
            - "off": No templating (default)
            - "explicit": Only Template instances
            - "all": Template all strings (dangerous!)
        **kwargs: Template variables if templating is enabled
    """
    match obj:
        case Template() if template_mode != "off":
            return render_prompt(obj, kwargs)

        case str() if template_mode == "all":
            return render_prompt(obj, kwargs)

        case str():
            return obj
        case type() if hasattr(obj, "__prompt_type__"):
            return obj.__prompt_type__()

        case _ if hasattr(obj, "__prompt__"):
            return obj.__prompt__()  # pyright: ignore[reportAttributeAccessIssue]

        case datetime():
            return obj.isoformat()

        case re.Pattern():
            flags = []
            if obj.flags & re.IGNORECASE:
                flags.append("ignorecase")
            if obj.flags & re.MULTILINE:
                flags.append("multiline")
            if obj.flags & re.DOTALL:
                flags.append("dotall")
            if obj.flags & re.VERBOSE:
                flags.append("verbose")
            flags_str = f" ({', '.join(flags)})" if flags else ""
            return f"Pattern: {obj.pattern!r}{flags_str}"

        case BasePrompt():
            messages = await obj.format(kwargs)
            return "\n".join(msg.get_text_content() for msg in messages)

        case type() if issubclass(obj, SQLModel):  # SQLModel class
            return generate_schema_description(obj)

        case _ if isinstance(obj, SQLModel):  # SQLModel instance
            # Get class documentation first
            schema_doc = generate_schema_description(obj.__class__)
            # Add current values
            values = "\nCurrent Values:\n"
            for field_name, value in obj.__dict__.items():
                if not field_name.startswith("_"):
                    values += f"- {field_name}: {value!r}\n"
            return schema_doc + values

        case _ if is_cli_object(obj):
            cmd_info = get_cmd_info(obj)
            if cmd_info is None:
                msg = f"Could not get CLI info for {type(obj)}"
                raise ValueError(msg)
            return format_cli_command(cmd_info)

        case _ if can_format_fields(obj):
            return format_dataclass_like(obj)
        case dict():
            results = await asyncio.gather(*(to_prompt(v) for k, v in obj.items()))
            return "\n".join(f"{k}: {r}" for (k, _), r in zip(obj.items(), results))

        case _ if is_sqlite_db(obj):
            # Pass the connection directly for in-memory databases
            return get_sqlite_schema(obj)  # type: ignore

        case list() | tuple():
            items = await asyncio.gather(*(to_prompt(item) for item in obj))
            return "\n".join(items)

        case Coroutine():
            result = await obj
            return await to_prompt(result, **kwargs)

        case _ if callable(obj):
            result = obj()
            return await to_prompt(result, **kwargs)

        case _:
            return str(obj)


def render_prompt(
    template: str,
    agent_context: dict[str, Any],
) -> str:
    """Render a prompt template with context.

    Available variables:
        agent.name: Name of the agent
        agent.id: Number of the clone (for cloned agents)
        agent.model: Model name
    """
    from jinja2 import Environment

    env = Environment(autoescape=True, keep_trailing_newline=True)
    tpl = env.from_string(template)
    return tpl.render(agent=agent_context)


def can_format_fields(obj: Any) -> bool:
    """Check if object can be inspected by fieldz."""
    try:
        get_adapter(obj)
    except TypeError:
        return False
    else:
        return True


def format_fastapi_app(app: Any) -> str:
    """Generate human-readable documentation from FastAPI application."""
    schema = app.openapi()
    lines = ["FastAPI Application Schema:"]

    # Info section
    if info := schema.get("info", {}):
        if title := info.get("title"):
            lines.append(f"\nTitle: {title}")
        if description := info.get("description"):
            lines.append(f"Description: {description}")
        if version := info.get("version"):
            lines.append(f"Version: {version}")

    # Endpoints
    lines.append("\nEndpoints:")
    paths = schema.get("paths", {})
    for path, methods in paths.items():
        lines.append(f"\n{path}")
        for method, details in methods.items():
            method_upper = method.upper()
            desc = details.get("description", "No description")
            lines.append(f"  {method_upper}: {desc}")

            # Parameters
            if params := details.get("parameters"):
                lines.append("  Parameters:")
                for param in params:
                    req = "*" if param.get("required") else ""
                    param_type = param.get("schema", {}).get("type", "any")
                    lines.append(
                        f"    - {param['name']}{req}: {param_type} "
                        f"({param.get('description', 'No description')})"
                    )

            # Request body
            if (body := details.get("requestBody")) and (
                ref := (
                    body.get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                    .get("$ref")
                )
            ):
                schema_name = ref.split("/")[-1]
                lines.append(f"  Request Body: {schema_name}")

            # Responses
            if responses := details.get("responses"):
                lines.append("  Responses:")
                for status, response in responses.items():
                    desc = response.get("description", "No description")
                    lines.append(f"    {status}: {desc}")
                    if ref := (
                        response.get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                        .get("$ref")
                    ):
                        schema_name = ref.split("/")[-1]
                        lines.append(f"      Schema: {schema_name}")

    return "\n".join(lines)
