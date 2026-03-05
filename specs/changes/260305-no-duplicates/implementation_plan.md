# Execution Duplication Plan

## Objective
Prevent overlapping or concurrent workday workflows from being instantiated if the user mistakenly sends the `/start` command twice.

## Requirements
- Introduce a tracking mechanism for active run states.
- Reject new `/start` signals if the state is marked as running.
- Provide clear Telegram feedback that a workday is already in progress.

## Steps
1. Maintain an internal `active_task` state flag or thread reference.
2. In the `start_command_handler`, verify if `active_task` is `None` or completed.
3. Reject overlap by routing a predefined error text to the user.
