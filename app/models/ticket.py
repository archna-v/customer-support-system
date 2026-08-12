class Ticket:
    VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]

    def __init__(self, title, description, priority):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError("Invalid priority")

        self.title = title
        self.description = description
        self.priority = priority
        self.status = "Open"

    def display_ticket(self):
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Priority: {self.priority}")
        print(f"Status: {self.status}")

    def close_ticket(self):
        self.status = "Closed"