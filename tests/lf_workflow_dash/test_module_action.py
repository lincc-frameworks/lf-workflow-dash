import os

import pytest

from lf_workflow_dash.data_types import read_yaml_file
from lf_workflow_dash.update_dashboard import update_html


@pytest.mark.parametrize(
    "datafile, outfile",
    [
        ("tracked_workflows_group.yaml", "lincc_output.html"),
        ("rail_tracked_workflows_group.yaml", "rail_output.html"),
        # ("tracked_incubator_group.yaml", "incubator_output.html")
    ],
)
def test_do_the_work(datafile, outfile, tmp_path):
    output_path = os.path.join(tmp_path, outfile)
    context = read_yaml_file(datafile)
    update_html(output_path, context)
