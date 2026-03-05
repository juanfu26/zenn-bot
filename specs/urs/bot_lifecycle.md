# Main Application Lifecycle

## 1. Purpose
The system automates Sign-In and Sign-Out actions on the Zenn platform, simulating a full workday via Telegram commands.

## 2. Process Flow
The bot operates as a state machine driven by user chat events and timers:

1. **Activation (`/start`)**: The user starts the workday. A separate thread launches to keep the bot responsive.  
2. **Sign-In**: The system navigates to the site, validates credentials, and ensures the current state is "clocked in".  
3. **Wait**: The system computes a randomized wait to simulate a real workday.  
4. **Sign-Out**: After the wait time collapses, the system performs the Sign-Out sequence.

## 3. Telegram Commands Reference
- `/start` — Starts the workday flow (Sign-In → Wait → Sign-Out).  
- `/status` — Reports the exact time remaining until automatic Sign-Out.  
- `/cancel` — Stops the current execution and clears active tasks safely.

## 4. Resilience Framework
- **Visual Evidence:** On any Playwright navigation error the system captures a screenshot (`error.png`) and sends it via Telegram along with contextual error details.  
- **Graceful Shutdown:** The script responds to `SIGINT` and `SIGTERM`. On OS shutdown it notifies the user logically and clears active timers to avoid inconsistent start/end states mapping.  
- **Timeouts:** All web selector waits are hard-capped at 60 seconds to prevent Playwright threads from hanging indefinitely.
