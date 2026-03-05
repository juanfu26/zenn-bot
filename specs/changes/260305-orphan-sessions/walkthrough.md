# Session Management Walkthrough

## 1. Initial State
The bot occasionally failed the login process if the session cookies persisted or a previous instance died mid-execution, leaving the user already logged in visually. This caused the script to stall looking for the credential inputs.

## 2. Implementation
- In the Playwright navigation sequence, an intermediate check was added before entering the username and password.
- Using `page.locator()`, the bot scans for the sign-out icon.
- If the icon is detected, the bot executes a click to fully log out and waits for the login page to fully render before continuing.

## 3. Conclusion
The bot can now recover from messy previous states or manual browser logins, ensuring robustness during the `/start` flow.
