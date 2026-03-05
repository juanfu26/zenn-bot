# Implementation Plan: Refactoring Zenn-Bot Text and Methodology

## Background
The user requested refactoring of log messages and Telegram chat messages in `main.py`. The requirements were:
1. Remove all references to "Phases" (Phase 1, Phase 2, Phase 3).
2. Improve function/method names to be readable and self-descriptive.
3. Centralize text messages in a separate file to keep the main code clean.
4. Translate all messages and code concepts to English consistently.
5. Update documentation files to reflect these changes.

## Execution Steps Taken

### Step 1: Centralize Messages
- Created a new file `messages.py`.
- Extracted all Telegram strings and logging formats from `main.py` into constant variables in `messages.py`.
- Defined logs with the prefix `LOG_` and Telegram messages with the prefix `TG_`.

### Step 2: Refactor `main.py`
- Imported `messages.py` into `main.py` as `msg`.
- Replaced all hardcoded string invocations (for `logger.info`, `logger.error`, `bot_send`, and `bot.reply_to`) with the corresponding constants from `msg`.
- Renamed methods to clearly indicate their function:
  - `run_phase_1` -> `perform_sign_in`
  - `run_phase_3` -> `perform_sign_out`
  - `run_full_shift` -> `execute_workday_cycle`

### Step 3: English Localization
- Assured that all texts in `messages.py` were fully translated and maintained in English. 
- Ensured consistency across logs and chat outputs (e.g. changing "Pantallazo tras el Sign-Out" to "Screenshot after Sign-Out").

### Step 4: Documentation Update
- Updated `docs/architecture.md` and `docs/business_logic.md`.
- Removed references to "Phase 1 - Smart Sign-In", "Phase 2 - Random Wait", and "Phase 3 - Automatic Sign-Out".
- Replaced them with the conceptual components "Sign-In", "Wait", and "Sign-Out".
- Validated that everything remains coherent with the codebase.

## Future Recommendations
- If multi-language support is ever needed, `messages.py` can be refactored into localization JSON dictionaries or standard Python `gettext`.
- For now, the abstraction successfully decouples business logic from presentation.
