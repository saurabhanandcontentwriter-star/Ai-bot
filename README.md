# Personal Assistant Chatbot

A simple **Python CLI chatbot** that acts like a personal assistant.

## Features
- Greeting and help commands
- Date and time lookup
- To-do management (add/list/remove)
- Notes management (add/list/remove)
- Motivation command
- Data persistence in `assistant_data.json`

## Run
```bash
python3 assistant_bot.py
```

## Example commands
- `hello`
- `help`
- `add todo buy groceries`
- `list todos`
- `remove todo 1`
- `add note Mom's birthday on Friday`
- `list notes`
- `remove note 1`
- `motivation`
- `bye`

## Test
```bash
python3 -m pytest -q
```
