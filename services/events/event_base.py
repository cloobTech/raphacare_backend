from collections import defaultdict, deque
from schemas.event import Event


class ServerSendEvent:
    """Server event schema with user-based events"""
    EVENT_QUEUES = defaultdict(deque)

    @staticmethod
    def print_event_queue():
        """Print event queue"""
        print(ServerSendEvent.EVENT_QUEUES)

    @staticmethod
    def add_event(user_id: str, event: Event):
        """Add event to the queue for a specific user"""
        ServerSendEvent.EVENT_QUEUES[user_id].append(event)

    @staticmethod
    def get_event(user_id: str):
        """Get event for a specific user"""
        if user_id in ServerSendEvent.EVENT_QUEUES and ServerSendEvent.EVENT_QUEUES[user_id]:
            return ServerSendEvent.EVENT_QUEUES[user_id].popleft()
        return None

    @staticmethod
    def clear_events(user_id: str):
        """Clear events for a specific user"""
        if user_id in ServerSendEvent.EVENT_QUEUES:
            ServerSendEvent.EVENT_QUEUES[user_id].clear()
            return True
        return False

    @staticmethod
    def count_events(user_id: str):
        """Count events for a specific user"""
        if user_id in ServerSendEvent.EVENT_QUEUES:
            return len(ServerSendEvent.EVENT_QUEUES[user_id])
        return 0
