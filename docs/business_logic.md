# Workday Agent — Functional Specifications

This document describes the business logic and functional specifications for the attendance automation bot for the Zenn platform.

## 1. Purpose
The system automates Sign-In and Sign-Out actions on the Zenn platform, simulating a full workday via Telegram commands.

## 2. Process Flow (Workday Lifecycle)
The bot operates as a state machine driven by events and timers:

1. **Activation (`/start`)**: The user starts the workday. A separate thread launches to keep the bot responsive.  
2. **Phase 1 — Smart Sign-In**: The system navigates to the site, validates credentials, and ensures the current state is "clocked in".  
3. **Phase 2 — Random Wait**: The system computes a randomized wait to simulate a real workday.  
4. **Phase 3 — Automatic Sign-Out**: After the wait, the system performs the Sign-Out sequence.

## 3. Business Rules
- **RN-01 — Access Control:** The bot only responds to a specific `USER_ID` defined via environment variables. All other users receive an "Access Denied" message.  
- **RN-02 — Orphan Sessions:** If a previous session is detected (e.g., a sign-out icon present), the bot first closes that session before starting a new one.  
- **RN-03 — Human Simulation:** Workday duration is randomized between 575 and 595 minutes ($9.75 \text{ hours} \pm 10 \text{ min}$) to avoid fixed robotic patterns and meet the target hours.
- **RN-04 — No Duplicates:** A new `/start` cannot be started if a task is already active for the same user.  
- **RN-05 — Safe Interruption:** The `/cancel` command stops the Phase 2 timer immediately and aborts Phase 3 (Sign-Out).

## 4. Telegram Commands
- `/start` — Starts the workday flow (Phase 1 → Phase 2 → Phase 3).  
- `/status` — Reports the exact time remaining until automatic Sign-Out.  
- `/cancel` — Stops the current execution and clears active tasks.

## 5. Error Handling and Resilience
- **Visual Evidence:** On any Playwright navigation error the system captures a screenshot (`error.png`) and sends it via Telegram along with error details.  
- **Graceful Shutdown:** The script handles `SIGINT` and `SIGTERM`. On shutdown it notifies the user and clears active timers to avoid inconsistent state.  
- **Timeouts:** Web selector waits are capped at 60 seconds to prevent indefinite hangs.
