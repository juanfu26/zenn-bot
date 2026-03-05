# Safe Interruption Plan

## Objective
Provide the user with a reliable "kill switch" to immediately halt an active workday simulation and exit cleanly without causing orphaned browser processes or incorrect Zenn portal states.

## Requirements
- Introduce a `/cancel` command to stop the main loop execution.
- If cancelled during the `Wait` period, the bot will NOT attempt a Sign-Out logic sequence.
- Clean up any threads and reset internal `active_task` states immediately.

## Steps
1. Listen for the `/cancel` Telegram command.
2. In the handler, identify the running thread/timer for the user.
3. Terminate or flag the thread to exit gracefully.
4. Notify the user of the cancellation.
