# Security Walkthrough

## 1. Initial State
The Telegram endpoint could be openly messaged by anyone who discovered the bot username, leading to unauthorized start actions and resource consumption.

## 2. Implementation
- We retrieved `TELEGRAM_USER_ID` using `os.getenv()`.
- Implemented a check condition in the `pyTelegramBotAPI` handlers to compare the sender's ID with the authorized ID.
- Configured a default "Access denied" string to return to illegitimate senders.
- Updated `compose.yml` and `.env` to define this ID securely.

## 3. Conclusion
The bot is now secure and strictly single-tenant. Unauthorized interactions are logged and immediately blocked.
