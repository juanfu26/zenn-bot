# Timezone Walkthrough

## 1. Initial State
The user needed the Docker container to execute actions accurately with the `Europe/Madrid` timezone, without losing track of changes bound by Daylight Saving Time (`DST`). Previously, without specifying a timezone, the container fell back to `UTC`, causing potential mismatch in task executions when Spanish daylight savings took effect.

## 2. Dockerfile Configuration
To allow the container to compute local offsets appropriately, native geographic rules were required within the Ubuntu base. We edited the existing `Dockerfile`:
- Added the line `ENV TZ=Europe/Madrid`.
- Installed `tzdata` utilizing `apt-get` directly from Ubuntu sources.
- Generated the local `/etc/localtime` pointer referencing the Madrid regional rules file and removed apt-caches to shrink layer sizes.

## 3. compose.yml Adjustments 
It was essential to feed the `TZ` environment to the Docker daemon when executing the `docker compose up` command.
- We inserted `TZ=Europe/Madrid` into the `environment` array block of `compose.yml`.
- This enforces the application context so any running Python scripts natively adopt Madrid's timezone variables. 

## 4. Conclusion
With these specific improvements deployed, all time tracking, log events spanning `datetime` features, and simulated sleep functionalities will effectively shift $\pm 1$ hour automatically each March and October according to standard DST mandates.
