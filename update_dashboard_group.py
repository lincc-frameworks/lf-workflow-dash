import sys

from jinja2 import Environment, FileSystemLoader

from lf_workflow_dash.data_types import read_yaml_file
from lf_workflow_dash.github_request import update_workflow_status


def update_html(out_file, context):
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("dash_template.jinja")
    with open(out_file, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))


def update_status(context, token):
    for project in context["all_projects"]:
        update_workflow_status(project.smoke_test, token)
        update_workflow_status(project.build_docs, token)
        update_workflow_status(project.benchmarks, token)
        update_workflow_status(project.live_build, token)
        for other_wf in project.other_workflows:
            update_workflow_status(other_wf, token)


def do_the_work(token, datafile, outfile):
    context = read_yaml_file(datafile)
    update_status(context, token)
    update_html(outfile, context)


if __name__ == "__main__":
    TOKEN = sys.argv[1]
    DATA_FILE = sys.argv[2]
    OUT_FILE = sys.argv[3]
    do_the_work(TOKEN, DATA_FILE, OUT_FILE)
