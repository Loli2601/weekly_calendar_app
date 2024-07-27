import pytest
from app import Calendar  # Import your Calendar class or functions

def test_create_calendar():
    calendar = Calendar()
    assert calendar is not None

def test_add_event():
    calendar = Calendar()
    event = {"title": "Meeting", "date": "2024-07-28", "time": "10:00"}
    calendar.add_event(event)
    assert len(calendar.events) == 1
    assert calendar.events[0] == event

def test_remove_event():
    calendar = Calendar()
    event = {"title": "Meeting", "date": "2024-07-28", "time": "10:00"}
    calendar.add_event(event)
    calendar.remove_event(event)
    assert len(calendar.events) == 0

def test_get_events_for_day():
    calendar = Calendar()
    event1 = {"title": "Meeting", "date": "2024-07-28", "time": "10:00"}
    event2 = {"title": "Lunch", "date": "2024-07-28", "time": "12:00"}
    event3 = {"title": "Dinner", "date": "2024-07-29", "time": "19:00"}
    calendar.add_event(event1)
    calendar.add_event(event2)
    calendar.add_event(event3)
    events = calendar.get_events_for_day("2024-07-28")
    assert len(events) == 2
    assert event1 in events
    assert event2 in events
    assert event3 not in events