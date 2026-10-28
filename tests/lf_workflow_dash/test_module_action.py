import os

import pytest

from lf_workflow_dash.update_dashboard import do_the_work


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
    do_the_work("TEST", datafile, output_path)
