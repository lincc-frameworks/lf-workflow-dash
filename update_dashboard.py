import sys

from lf_workflow_dash.update_dashboard import do_the_work

if __name__ == "__main__":
    TOKEN = sys.argv[1]
    DATA_FILE = sys.argv[2]
    OUT_FILE = sys.argv[3]
    do_the_work(TOKEN, DATA_FILE, OUT_FILE)
