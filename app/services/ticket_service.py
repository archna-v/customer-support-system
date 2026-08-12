from datetime import datetime, timezone

from bson import ObjectId

from app.database.mongodb import tickets_collection
from app.core.logger import logger


def serialize_ticket(ticket):

    if ticket is None:
        return None

    ticket["_id"] = str(ticket["_id"])

    if ticket.get("created_at"):
        ticket["created_at"] = ticket["created_at"].isoformat()

    if ticket.get("updated_at"):
        ticket["updated_at"] = ticket["updated_at"].isoformat()

    return ticket


def create_ticket(ticket):

    now = datetime.now(timezone.utc)

    ticket_data = {
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority,
        "status": "Open",
        "created_at": now,
        "updated_at": now
    }

    result = tickets_collection.insert_one(ticket_data)

    ticket_id = str(result.inserted_id)

    logger.info(
        f"Ticket created successfully: {ticket_id}"
    )

    return {
        "message": "Ticket created successfully",
        "ticket_id": ticket_id,
        "ticket": {
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority,
            "status": "Open",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
    }


def get_all_tickets(
    search=None,
    priority=None,
    status=None,
    page=1,
    limit=10
):

    logger.info(
        f"Fetching tickets - search={search}, priority={priority}, "
        f"status={status}, page={page}, limit={limit}"
    )

    query = {}

    if priority:
        query["priority"] = priority

    if status:
        query["status"] = status

    if search:
        query["$or"] = [
            {
                "title": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "description": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    total = tickets_collection.count_documents(query)

    skip = (page - 1) * limit

    tickets = list(
        tickets_collection
        .find(query)
        .skip(skip)
        .limit(limit)
    )

    for ticket in tickets:
        serialize_ticket(ticket)

    total_pages = (total + limit - 1) // limit

    return {
        "count": len(tickets),
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "tickets": tickets
    }


def get_ticket(ticket_id):

    logger.info(
        f"Fetching ticket: {ticket_id}"
    )

    try:
        object_id = ObjectId(ticket_id)
    except Exception:
        logger.warning(
            f"Invalid ticket ID: {ticket_id}"
        )
        return None, "Invalid ticket ID"

    ticket = tickets_collection.find_one({
        "_id": object_id
    })

    if ticket is None:
        logger.warning(
            f"Ticket not found: {ticket_id}"
        )
        return None, "Ticket not found"

    serialize_ticket(ticket)

    logger.info(
        f"Ticket fetched successfully: {ticket_id}"
    )

    return ticket, None


def update_ticket(ticket_id, ticket):

    logger.info(
        f"Updating ticket: {ticket_id}"
    )

    try:
        object_id = ObjectId(ticket_id)
    except Exception:
        logger.warning(
            f"Invalid ticket ID for update: {ticket_id}"
        )
        return None, "Invalid ticket ID"

    update_data = {
        key: value
        for key, value in ticket.model_dump().items()
        if value is not None
    }

    if not update_data:
        logger.warning(
            f"No fields provided for ticket update: {ticket_id}"
        )
        return None, "No fields provided for update"

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = tickets_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        logger.warning(
            f"Ticket not found for update: {ticket_id}"
        )
        return None, "Ticket not found"

    updated_ticket = tickets_collection.find_one(
        {"_id": object_id}
    )

    serialize_ticket(updated_ticket)

    logger.info(
        f"Ticket updated successfully: {ticket_id}"
    )

    return updated_ticket, None

def delete_ticket(ticket_id):

    logger.info(
        f"Deleting ticket: {ticket_id}"
    )

    try:
        object_id = ObjectId(ticket_id)
    except Exception:
        logger.warning(
            f"Invalid ticket ID for deletion: {ticket_id}"
        )
        return False, "Invalid ticket ID"

    result = tickets_collection.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        logger.warning(
            f"Ticket not found for deletion: {ticket_id}"
        )
        return False, "Ticket not found"

    logger.info(
        f"Ticket deleted successfully: {ticket_id}"
    )

    return True, None
