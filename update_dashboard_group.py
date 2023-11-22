import sys

from jinja2 import Environment, FileSystemLoader

from lf_workflow_dash.update_dashboard import do_the_work

if __name__ == "__main__":
    TOKEN = sys.argv[1]
    TOKEN = "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"
    DATA_FILE = sys.argv[2]
    OUT_FILE = sys.argv[3]
    do_the_work(TOKEN, DATA_FILE, OUT_FILE)
