from jinja2 import Environment, FileSystemLoader

from lf_workflow_dash.data_types import read_yaml_file
from lf_workflow_dash.github_request import update_workflow_status


def update_html(out_file, context):
    """Fetch the jinja template, and update with all of the gathered context.

    Args:
        out_file (str): path to write the hydrated html file to
        context (dict): local variables representing workflow status
    """
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("dash_template.jinja")
    with open(out_file, mode="w", encoding="utf-8") as results:
        results.write(template.render(context))


def update_status(context, token):
    """Issue requests to the github JSON API and update each workflow status accordingly.

    Args:
        context (dict): local variables representing workflow status
        token (str): github personal access token
    """
    for project in context["all_projects"]:
        print(project.repo)
        update_workflow_status(project.smoke_test, token)
        update_workflow_status(project.build_docs, token)
        update_workflow_status(project.benchmarks, token)
        update_workflow_status(project.live_build, token)
        for other_wf in project.other_workflows:
            update_workflow_status(other_wf, token)


def do_the_work(token, datafile, outfile):
    """Wrapper to call all of the methods necessary to build the final hydrated page.

    Args:
        token (str): github personal access token
        datafile (str): path to the yaml config file with workflow data
        outfile (str): write to write the hyrated html file to
    """
    context = read_yaml_file(datafile)
    update_status(context, token)
    update_html(outfile, context)
