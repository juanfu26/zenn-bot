# Security Plan

## Objective
Ensure that the Telegram bot only processes messages and commands originating from the authorized user as specified in the environment variables.

## Requirements
- Match the incoming message `chat.id` against the configured `TELEGRAM_USER_ID`.
- Handle unauthorized access by returning an "Access Denied" message and ignoring further input.
- Secure environment configuration using `compose.yml` to prevent hardcoded credentials.

## Steps
1. Store the allowed User ID in `TELEGRAM_USER_ID` env var.
2. In `main.py`, implement an authorization decorator or check at the beginning of every command handler.
3. Terminate requests that do not pass the check.
