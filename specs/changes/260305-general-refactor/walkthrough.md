# Walkthrough: Refactoring Zenn-Bot Strings & Flow

This walkthrough explains how the string centralization and method renaming was performed in the Zenn Auto-Clockout Agent.

## 1. Creating `messages.py`
To avoid scattering text (both log lines and user-facing Telegram messages) across the bot's logic, a dedicated constants file was introduced.
```python
# app/messages.py
# --- LOG MESSAGES ---
LOG_START_SIGN_IN = "[{}] Starting Smart Sign-In"
...
# --- TELEGRAM MESSAGES ---
TG_SIGN_IN_CONFIRMED = "✅ Standard Sign-In confirmed."
TG_STARTING_SIGN_IN = "🚀 Ensuring Sign-In..."
```
Benefits: Easily update typos, change emojis, or rewrite messages without touching the Playwright logic.

## 2. Refactoring Method Names
Before, the code mapped business logic to "Phases":
- `run_phase_1`
- `run_phase_3`
- `run_full_shift`

These were transformed into action-based verbs for maintainability:
- `perform_sign_in`
- `perform_sign_out`
- `execute_workday_cycle`

## 3. String Replacement in `main.py`
In `app/main.py`, the `messages` module is imported:
```python
import messages as msg
```
And wherever a string was previously formatted or sent, it uses `.format()` on the constant:
```python
def perform_sign_in(chat_id):
    logger.info(msg.LOG_START_SIGN_IN.format(chat_id))
    # ... playwright setup
    bot_send(chat_id, msg.TG_STARTING_SIGN_IN)
```

## 4. Documentation Alignment
The Markdown files (`docs/architecture.md` and `docs/business_logic.md`) were manually updated to reflect the deprecation of the "Phase" vocabulary, unifying the application's domain language to:
- **Sign-In**
- **Wait**
- **Sign-Out**

This brings the technical documentation into exact correspondence with the actual implementation and terminology used throughout the codebase.
