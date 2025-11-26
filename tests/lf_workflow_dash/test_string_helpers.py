import os
from pathlib import Path

from semver import Version

from lf_workflow_dash.string_helpers import coerce_copier_version, get_conclusion_time, read_copier_version

TEST_DIR = os.path.dirname(__file__)


def test_get_conclusion_time():
    time, stale = get_conclusion_time({"updated_at": "2024-09-23T06:52:27Z"})
    assert stale
    assert time == "02:52<br>09/23/24"


COPIER_FILE_CONTENT = """_commit: v2.1.0
_src_path: gh:lincc-frameworks/python-project-template
author_email: lincc-frameworks-team@lists.lsst.org
author_name: LINCC Frameworks
create_example_module: false
custom_install: true"""


def test_read_copier_version_good():
    test_file_path = Path(TEST_DIR).parent.parent / ".copier-answers.yml"
    with open(test_file_path, "r", encoding="utf-8") as file:
        data = file.read()
        copier_version_string = read_copier_version(data)
        assert copier_version_string.startswith("v")

    copier_version_string = read_copier_version(COPIER_FILE_CONTENT)
    assert copier_version_string == "v2.1.0"

    copier_version_string = read_copier_version("_commit: v2.1.0")
    assert copier_version_string == "v2.1.0"


def test_read_copier_version_bad():
    copier_version_string = read_copier_version("nothing to see here")
    assert copier_version_string == ""

    copier_version_string = read_copier_version("yaml: yes")
    assert copier_version_string == ""


def test_coerce_copier_version_good():
    copier_version_string = coerce_copier_version("v2.1.0")
    assert copier_version_string == Version(2, 1, 0)

    copier_version_string = coerce_copier_version("2.1.0")
    assert copier_version_string == Version(2, 1, 0)

    copier_version_string = coerce_copier_version("V2.1.0")
    assert copier_version_string == Version(2, 1, 0)

    copier_version_string = coerce_copier_version("version2.1.0")
    assert copier_version_string == Version(2, 1, 0)

    copier_version_string = coerce_copier_version("V2.1")
    assert copier_version_string == Version(2, 1)


def test_coerce_copier_version_bad():
    copier_version_string = coerce_copier_version("yaml: yes")
    assert copier_version_string is None

    copier_version_string = coerce_copier_version(None)
    assert copier_version_string is None

    copier_version_string = coerce_copier_version("")
    assert copier_version_string is None
