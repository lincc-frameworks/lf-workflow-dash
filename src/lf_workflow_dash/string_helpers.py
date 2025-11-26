import re
from datetime import datetime

import pytz
import yaml
from semver import Version


def get_conclusion_time(last_run):
    """Get the workflow conclusion time and set the proper timezone

    Args:
        last_run (dict): the most recent run of the workflow
    """
    timestamp_str = last_run["updated_at"]

    # Parse the timestamp
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")

    # Define the time zones for UTC and New York
    utc_timezone = pytz.timezone("UTC")
    ny_timezone = pytz.timezone("America/New_York")

    # Convert the timestamp to New York time
    timestamp_ny = timestamp.replace(tzinfo=utc_timezone).astimezone(ny_timezone)

    # Format the timestamp
    formatted_timestamp = timestamp_ny.strftime("%H:%M<br>%m/%d/%y")

    # Figure out how old this conclusion time is. If it's more than 2 weeks, it's stale.
    current_date = datetime.now()
    date_diff = current_date - timestamp
    is_stale = date_diff.days > 14

    return (formatted_timestamp, is_stale)


BASEVERSION = re.compile(
    r"""[vV]?
        (?P<major>0|[1-9]\d*)
        (\.
        (?P<minor>0|[1-9]\d*)
        (\.
            (?P<patch>0|[1-9]\d*)
        )?
        )?
    """,
    re.VERBOSE,
)


def coerce_copier_version(input_semver):
    """Coerce a version string into a semantic version object.

    Allows for strings with `v` or ``version` at the start of the string."""
    if not input_semver:
        return None
    match = BASEVERSION.search(input_semver)
    if not match:
        return None

    ver = {key: 0 if value is None else value for key, value in match.groupdict().items()}
    ver = Version(**ver)
    return ver


def read_copier_version(content):
    """Read the `_commit` from a copier answers config file."""
    try:
        copier_config = yaml.safe_load(content)
        copier_version = copier_config.get("_commit", "")
        print("   copier version:", copier_version)
        return copier_version
    except yaml.YAMLError:
        return ""
    except AttributeError:
        return ""
