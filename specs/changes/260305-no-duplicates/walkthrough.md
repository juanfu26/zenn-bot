# Execution Duplication Walkthrough

## 1. Initial State
A user typing `/start` while the bot was already looping/waiting caused Playwright to crash or double-execute the login routine leading to parallel timers and confused states.

## 2. Implementation
- An application-level dictionary or object tracks active work cycles via `user_id`.
- The `/start` endpoint checks this structure before launching Playwright.
- If a cycle is detected, it aborts the new request and alerts the user to `Use /cancel to stop the active cycle first`.

## 3. Conclusion
Concurrency issues are mitigated and the bot architecture handles duplicate spam gracefully.
