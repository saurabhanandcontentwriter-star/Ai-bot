from assistant_bot import AssistantState, handle_message


def test_greeting():
    state = AssistantState()
    reply = handle_message("hello", state)
    assert "personal assistant bot" in reply.lower()


def test_add_and_list_todos():
    state = AssistantState()
    add_reply = handle_message("add todo practice english", state)
    assert "Added todo #1" in add_reply

    list_reply = handle_message("list todos", state)
    assert "1. practice english" in list_reply


def test_invalid_remove_note():
    state = AssistantState()
    reply = handle_message("remove note 1", state)
    assert reply == "Invalid note number."
