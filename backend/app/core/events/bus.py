import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict, List, Type, TypeVar
from app.core.events.events import BaseEvent

T = TypeVar("T", bound=BaseEvent)
EventListener = Callable[[T], Awaitable[None]]


class EventBus:
    """In-process asynchronous publish-subscribe Event Bus for domain events."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[EventListener[Any]]] = {}
        self.logger = logging.getLogger(__name__)

    def subscribe(
        self, event_type: Type[BaseEvent], listener: EventListener[Any]
    ) -> None:
        """Register a callback coroutine to handle a specific event type."""
        event_name = event_type.__name__
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)
        self.logger.debug(f"Subscribed callback to event: {event_name}")

    async def publish(self, event: BaseEvent) -> None:
        """Asynchronously dispatch an event to all subscribed listeners."""
        event_name = event.__class__.__name__
        listeners = self._listeners.get(event_name, [])

        if not listeners:
            self.logger.debug(f"Event {event_name} published but has no subscribers.")
            return

        self.logger.info(
            f"EventBus: Publishing '{event_name}' [ID: {event.event_id}] "
            f"Trace-ID: '{event.correlation_id or 'none'}'"
        )

        # Invoke all callbacks concurrently in isolated execution wrappers
        tasks = [self._run_listener(listener, event) for listener in listeners]
        await asyncio.gather(*tasks)

    async def _run_listener(
        self, listener: EventListener[Any], event: BaseEvent
    ) -> None:
        """Execute listener coroutine, catching exceptions to protect event dispatch thread."""
        try:
            await listener(event)
        except Exception as e:
            self.logger.error(
                f"EventBus error: Handler '{listener.__name__ if hasattr(listener, '__name__') else 'unknown'}' "
                f"failed processing event '{event.__class__.__name__}': {e}",
                exc_info=True,
            )
