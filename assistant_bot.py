#!/usr/bin/env python3
"""Personal Assistant Chatbot (CLI).

Features:
- Natural small-talk style responses
- Date/time helper
- Persistent to-do list
- Persistent notes
- Basic motivation and help commands
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

DATA_FILE = Path("assistant_data.json")


@dataclass
class AssistantState:
    todos: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def load_state() -> AssistantState:
    if not DATA_FILE.exists():
        return AssistantState()

    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return AssistantState(
            todos=list(raw.get("todos", [])),
            notes=list(raw.get("notes", [])),
        )
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return AssistantState()


def save_state(state: AssistantState) -> None:
    payload = {"todos": state.todos, "notes": state.notes}
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def normalize(text: str) -> str:
    return text.strip().lower()


def render_help() -> str:
    return (
        "I can help with:\n"
        "- time / date\n"
        "- add todo <task>\n"
        "- list todos\n"
        "- remove todo <number>\n"
        "- add note <text>\n"
        "- list notes\n"
        "- remove note <number>\n"
        "- motivation\n"
        "- bye"
    )


def parse_index(message: str, command: str) -> int | None:
    match = re.match(rf"^{command}\s+(\d+)$", normalize(message))
    if not match:
        return None
    return int(match.group(1))


def handle_message(message: str, state: AssistantState) -> str:
    msg = normalize(message)

    if msg in {"hi", "hello", "hey"}:
        return "Hi! I'm your personal assistant bot. Type 'help' to see what I can do."

    if msg in {"help", "commands"}:
        return render_help()

    if msg in {"time", "what time is it", "current time"}:
        return f"Current time: {datetime.now().strftime('%I:%M %p')}"

    if msg in {"date", "today", "what is today's date"}:
        return f"Today's date: {datetime.now().strftime('%A, %d %B %Y')}"

    if msg.startswith("add todo "):
        task = message[9:].strip()
        if not task:
            return "Please provide a todo text, e.g. 'add todo buy milk'."
        state.todos.append(task)
        save_state(state)
        return f"Added todo #{len(state.todos)}: {task}"

    if msg == "list todos":
        if not state.todos:
            return "Your todo list is empty."
        lines = ["Your todos:"]
        for idx, task in enumerate(state.todos, start=1):
            lines.append(f"{idx}. {task}")
        return "\n".join(lines)

    todo_idx = parse_index(message, "remove todo")
    if todo_idx is not None:
        if todo_idx < 1 or todo_idx > len(state.todos):
            return "Invalid todo number."
        removed = state.todos.pop(todo_idx - 1)
        save_state(state)
        return f"Removed todo: {removed}"

    if msg.startswith("add note "):
        note = message[9:].strip()
        if not note:
            return "Please provide note text, e.g. 'add note call John at 5'."
        state.notes.append(note)
        save_state(state)
        return f"Saved note #{len(state.notes)}."

    if msg == "list notes":
        if not state.notes:
            return "You don't have notes yet."
        lines = ["Your notes:"]
        for idx, note in enumerate(state.notes, start=1):
            lines.append(f"{idx}. {note}")
        return "\n".join(lines)

    note_idx = parse_index(message, "remove note")
    if note_idx is not None:
        if note_idx < 1 or note_idx > len(state.notes):
            return "Invalid note number."
        removed = state.notes.pop(note_idx - 1)
        save_state(state)
        return f"Removed note: {removed}"

    if msg in {"motivation", "motivate me", "quote"}:
        return "You are doing better than you think. One small step now creates big results later."

    if msg in {"bye", "exit", "quit"}:
        return "Goodbye! Take care."

    return (
        "Sorry, I didn't understand that. Type 'help' to see available commands."
    )


def main() -> None:
    print("Personal Assistant Bot")
    print("Type 'help' for commands. Type 'bye' to exit.\n")

    state = load_state()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        response = handle_message(user_input, state)
        print(f"Bot: {response}")

        if normalize(user_input) in {"bye", "exit", "quit"}:
            break


if __name__ == "__main__":
    main()
