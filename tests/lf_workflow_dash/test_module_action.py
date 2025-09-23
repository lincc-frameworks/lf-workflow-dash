import os

import pytest

from lf_workflow_dash.data_types import read_yaml_file
from lf_workflow_dash.github_request import get_conclusion_time
from lf_workflow_dash.update_dashboard import update_html


@pytest.mark.parametrize(
    "datafile, outfile",
    [
        ("config/tracked_workflows.yaml", "lincc_output.html"),
        ("config/rail_tracked_workflows.yaml", "rail_output.html"),
        ("config/tracked_incubator.yaml", "incubator_output.html"),
        ("config/lsdb_workflows.yaml", "lsdb_output.html"),
    ],
)
def test_do_the_work(datafile, outfile, tmp_path):
    output_path = os.path.join(tmp_path, outfile)
    context = read_yaml_file(datafile)
    update_html(output_path, context)


def test_get_conclusion_time():
    time, stale = get_conclusion_time({"updated_at": "2024-09-23T06:52:27Z"})
    assert stale
    assert time == "02:52<br>09/23/24"
