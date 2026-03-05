# AI Agents Instructions

This document provides essential instructions, context, and standard operating procedures for AI coding assistants (such as Antigravity/Gemini) interacting with the `zenn-bot` repository.

## 1. Project Standards Location
All architectural designs, coding standards, and business logic documentation are centralized in the `specs/standards/` directory.
- **Architecture & Flow:** `specs/standards/architecture.md`

Always consult these files before proposing major refactors or adding new components.

## 2. Artifacts Persistence
Agents must use the designated artifact directory (typically `<appDataDir>/brain/<conversation-id>`) to persist their working documents while developing tasks.
- **`task.md`**: Maintain a detailed checklist of tasks. Mark items as `[ ]`, `[/]`, or `[x]`.
- **`implementation_plan.md`**: Outline your technical approach and proposed file changes (using `[NEW]`, `[MODIFY]`, `[DELETE]`). Request user approval before executing.
- **`walkthrough.md`**: Summarize completed work, verification steps, validation results, and any relevant logs or screenshots.

**Permanent Storage:** Once the implementation plan is fully executed and the review/walkthrough is completed, agents must persist both the `implementation_plan.md` and `walkthrough.md` files into the project source tree under `specs/changes/`. Create a dedicated directory for the completed task using an appropriate naming format, for example: `specs/changes/YYMMDD-taskname/`.

*Note:* Use the `/tmp/` directory for scratch scripts or one-off runs, keeping the main project directory clean.

## 3. Agent Workflow
Agents should follow a structured spec-driven development process:
1. **Planning (`PLANNING` mode):** Analyze requirements, read `specs/standards/`, create `task.md` to break down the work, and draft an `implementation_plan.md` for user approval.
2. **Execution (`EXECUTION` mode):** Implement the codebase modifications according to the plan. Make sure to keep `task.md` updated as items are worked on and completed.
3. **Verification (`VERIFICATION` mode):** Test and validate the implementation. Create or update `walkthrough.md` to record the testing outcome and provide proof of work.

## 4. Basic Project Aspects
- **Name:** Zenn Auto-Clockout Agent
- **Description:** A headless automation service running on Docker (Raspberry Pi target). It uses Playwright to interact with a web portal and Telebot to receive remote commands via Telegram.
- **Tech Stack:** Python 3.10+, Playwright (Chromium), `pyTelegramBotAPI`, Docker & Docker Compose.
- **Execution Rules:**
  - **Asynchronous/Threads:** Wait tasks (which can take hours) use Python's `threading` so the main Telegram bot listener isn't blocked.
  - **Playwright Navigation:** Handle timeouts gracefully (cap at 60s). Ensure clean context teardowns. Take screenshots and report to Telegram if critical errors occur.
  - **Absolute Paths:** Always use absolute file paths internally or paths relative to the script directory using `os.path`.
  - **Secrets:** Never hardcode secrets; read them from environment variables (`.env`).
  - **Logging:** Use standardized logging instead of plain `print()` statements.
