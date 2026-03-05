# Implementation Plan: Dynamic Shift Timings

## Objective
Implement dynamic calculation of the sign-out timer based on the current date, detecting summer periods, Fridays, and applying random delays as specified by the user's requirements.

## File Changes
- `[MODIFY]` **`app/main.py`**:
  - Read new environment variables for shift durations (`WORK_MINUTES_REGULAR`, `WORK_MINUTES_LUNCH`, `WORK_MINUTES_FRIDAY`, `WORK_MINUTES_SUMMER`, `WORK_RANDOM_DELAY_MAX`, `SUMMER_PERIOD_START`, `SUMMER_PERIOD_END`).
  - Add function `is_summer_period(now: datetime)` to determine if the specified summer period is active based on `MM-DD` configurations.
  - Update the wait logic inside `execute_workday_cycle` to select the correct base minutes based on the day of the week and the summer period state.
  - Apply the random delay to Monday-Thursday, Friday, and Summer Period setups.
- `[NEW]` **`.env.example`**:
  - Add an example environment configuration file to document the keys required for dynamic shift timings, preventing hardcoding.

## Verification
- Validate the behavior algorithm manually.
- Confirm variables are correctly loaded from the `.env` context.
