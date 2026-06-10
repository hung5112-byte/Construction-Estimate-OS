"""DEPRECATED (06/09/2026): one-time backfill of aliases_vn for the original 12
generic-business departments. The 5 hardware-division departments ship with
their aliases already set in departments/*/department.yaml — there is nothing
to backfill, and the old map would recreate stale department references.
Kept for build history only."""
import sys

sys.exit("DEPRECATED: aliases ship in the 5 division department.yaml files. Aborting.")
