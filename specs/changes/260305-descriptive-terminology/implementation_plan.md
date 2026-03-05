# Descriptive Terminology Plan

## Objective
Swap numerical phase notation ("Phase 1", "Phase 2") with descriptive function names indicating real actions ("Sign-In", "Wait", "Sign-Out") internally and to the user.

## Requirements
- Scan codebase and messaging structs for references to "Phase".
- Replace numerical references with the direct operational equivalents.
- Ensure logging traces these functional tags.

## Steps
1. Update Telegram outputs so `/status` indicates "Wait" instead of "Phase 2".
2. Update logs to read `Attempting Sign-Out` instead of `Entering Phase 3`.
