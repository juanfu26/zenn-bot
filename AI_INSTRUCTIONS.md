# AI Agent Instructions (Gemini & Antigravity)

These instructions are intended for AI coding assistants such as Gemini and Antigravity to ensure consistency and high code quality when maintaining and extending the `zenn-bot` repository.

## 1. Project Context & Rules
- **Name:** Zenn Auto-Clockout Agent
- **Description:** Headless automation service running on a Raspberry Pi using Docker. Triggers delayed clock-out actions on the Zenn HR portal via a Telegram Bot.
- **Documentation:** Always consult the following directories for specific domain knowledge before proposing major refactors:
  - `docs/architecture.md` -> Infrastructure, stack, execution flow.
  - `docs/business_logic.md` -> Timings, Telegram commands, error policies.

## 2. Coding Conventions
- **Language:** Python only.
- **Modularity:** Ensure clear separation of concerns (Interface, Logic, Automation).
- **Asynchronous Execution:** Heavy tasks (like waiting or browser automation) should be handled nicely without blocking the main Telegram bot listener thread. The codebase uses `threading` modules.
- **Error Handling:** Avoid silent failures. Catch exceptions and log them. For critical Playwright failures, always take a screenshot and report via Telegram.
- **Logging:** Use standardized logging rather than plain `print` statements to allow aggregation by Docker.
- **Paths:** Always use absolute file paths internally or `os.path` combinations relative to the script directory, avoiding assumptions about the current working directory.

## 3. Interaction with External Services
- **Playwright:** Use headless chromium. Navigation should handle timeouts gracefully (cap at 60s). Ensure clean context teardowns.
- **Telebot:** Adhere strictly to the `TELEGRAM_USER_ID` whitelist to prevent unauthorized access.
- **Secrets:** Never hardcode secrets in code. Always pull them from environment variables.

## 4. Agent Best Practices
- Before providing code snippets, always think through the steps to reproduce the exact issue described.
- Keep the `README.md` clean for human consumption.
- Maintain a concise, professional tone in commit messages and documentation.
