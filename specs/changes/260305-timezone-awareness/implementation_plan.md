# Timezone Implementation Plan

## Objective
Ensure the Docker container running the Zenn bot operates strictly within the `Europe/Madrid` timezone, and accurately reflects local time adjustments during Daylight Saving Time (DST) transitions automatically.

## Requirements
- Set environment variables to define the geographical location.
- Install native OS time zone data schemas (`tzdata`).
- Assure that both Python internal clocks and cron-like delays maintain accuracy with local time.

## Steps

1. **Modify Dockerfile**
   - Add the `TZ` environment variable to define the default timezone for system tools and libraries inside the build as `Europe/Madrid`.
   - Update package manager (`apt-get update`) and install `tzdata`.
   - Create symlink referencing the `Europe/Madrid` file from `/usr/share/zoneinfo/` to `/etc/localtime`.
   - Persist the timezone name into `/etc/timezone`.
   
2. **Modify compose.yml**
   - Explicitly define the `TZ` environment variable in the `zenn-bot` service definition under the `environment` section to `Europe/Madrid`.
   - This prevents overrides when the container launches and forces Docker to inject the correct timezone to the running instance.

## Output
By implementing these changes, any scripts running inside the Python process will correctly resolve `datetime.now()` and time-based sleep functionality relative to Spanish local time, without manual intervention during DST bounds.
