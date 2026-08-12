from pydantic import BaseModel, Field
from typing import Optional, Literal


class TicketCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=1000
    )

    priority: Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ]


class TicketUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=1000
    )

    priority: Optional[Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ]] = None

    status: Optional[Literal[
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]] = None