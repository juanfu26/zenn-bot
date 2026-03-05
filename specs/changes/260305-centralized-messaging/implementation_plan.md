# Centralized Messaging Plan

## Objective
Decouple hardcoded text output directly in business logic (like handling logins or wait states) from the content creation and Telegram formatting strings.

## Requirements
- Create a dedicated definitions dictionary or python module (`messages.py`).
- All text outputs bound to user responses or logs must utilize this centralized lookup.
- Ensures simple content updates without modifying logic code.

## Steps
1. Create `messages.py` isolating strings into explicit, descriptive constant variables.
2. Refactor `main.py` business components to import formatted constants instead of `f-strings` locally.
