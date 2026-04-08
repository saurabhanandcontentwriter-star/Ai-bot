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


## SEO Tools Module
This repo now includes `seo_tools.py` for accurate, testable SEO analysis.

### What it provides
- HTML on-page audit (`audit_html`)
- Keyword density calculation with exact matching (`keyword_density`)
- Word tokenization utility (`tokenize`)

### Quick example
```python
from seo_tools import audit_html

html = """<html><head><title>SEO Example Title for Better Visibility</title></head><body><h1>SEO Example</h1></body></html>"""
result = audit_html(html, ["seo example"])
print(result.score)
print(result.recommendations)
```
