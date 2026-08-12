from fastapi import APIRouter, HTTPException, Query, Depends

from app.services.ticket_service import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket,
    delete_ticket
)

from app.schemas.ticket import TicketCreate, TicketUpdate

from app.auth.auth_dependencies import (
    get_current_user,
    require_role
)


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# -----------------------------
# CREATE TICKET
# -----------------------------

@router.post("")
def create_new_ticket(
    ticket: TicketCreate,
    current_user: dict = Depends(get_current_user)
):
    return create_ticket(ticket)


# -----------------------------
# GET ALL TICKETS
# -----------------------------

@router.get("")
def get_tickets(
    search: str | None = Query(
        default=None,
        description="Search in ticket title and description"
    ),
    priority: str | None = Query(
        default=None,
        description="Filter by priority"
    ),
    status: str | None = Query(
        default=None,
        description="Filter by status"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of tickets per page"
    ),
    current_user: dict = Depends(get_current_user)
):
    return get_all_tickets(
        search=search,
        priority=priority,
        status=status,
        page=page,
        limit=limit
    )


# -----------------------------
# GET SINGLE TICKET
# -----------------------------

@router.get("/{ticket_id}")
def get_single_ticket(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):

    ticket, error = get_ticket(ticket_id)

    if error == "Invalid ticket ID":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    if error == "Ticket not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    return ticket


# -----------------------------
# UPDATE TICKET
# -----------------------------

@router.put("/{ticket_id}")
def update_existing_ticket(
    ticket_id: str,
    ticket: TicketUpdate,
    current_user: dict = Depends(
        require_role(["Support Agent", "Admin"])
    )
):

    updated_ticket, error = update_ticket(
        ticket_id,
        ticket
    )

    if error == "Invalid ticket ID":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    if error == "Ticket not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "No fields provided for update":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Ticket updated successfully",
        "ticket": updated_ticket
    }
# -----------------------------
# DELETE TICKET
# -----------------------------

@router.delete("/{ticket_id}")
def delete_existing_ticket(
    ticket_id: str,
    current_user: dict = Depends(
        require_role(["Admin"])
    )
):

    success, error = delete_ticket(ticket_id)

    if error == "Invalid ticket ID":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    if error == "Ticket not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    return {
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }