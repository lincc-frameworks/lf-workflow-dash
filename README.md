<!-- [![pages-build-deployment](https://github.com/OliviaLynn/lf-workflow-dash/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/OliviaLynn/lf-workflow-dash/actions/workflows/pages/pages-build-deployment) -->
<!-- ![GitHub issues](https://img.shields.io/github/issues/OliviaLynn/lf-workflow-dash) -->
<!-- [![codecov](https://codecov.io/gh/OliviaLynn/lf-workflow-dash/branch/master/graph/badge.svg)](https://codecov.io/gh/OliviaLynn/lf-workflow-dash) -->
<!-- ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OliviaLynn/lf-workflow-dash/ci.yml) -->

<img src="https://www.lsstcorporation.org/lincc/sites/default/files/PastedGraphic-8.png" width="300" height="100">

# LF Workflow Dash

[![view](https://img.shields.io/badge/view:-666666?style=for-the-badge)](#)
[![link-to-dash](https://img.shields.io/badge/LF_Dashboard-7b6db0?style=for-the-badge)](https://olivialynn.github.io/lf-workflow-dash/)
[![link-to-rail-dash](https://img.shields.io/badge/RAIL_Dashboard-b08b3d?style=for-the-badge)](https://olivialynn.github.io/lf-workflow-dash/rail.html)

**LF Workflow Dash** is your simple solution for monitoring and managing GitHub Actions workflows. 

Track workflows across any number of repositories, check status and other relevant metrics, and easily modify via yaml, all in one customizable dashboard.

Powered by the [GitHub REST API](https://docs.github.com/en/rest), **LF Workflow Dash** regularly retrieves data on specified GitHub Actions workflow runs and updates the dashboard HTML. This process is managed through scheduled GitHub workflows, and the output can be hosted easily using GitHub Pages."

## Getting Started

Click any of the badges at the top of the README to view a dashboard. 

Keep reading to learn about modifying an existing dashboard, or how to build your own dashboard.

## Modify the LF Dashboard

1. **Modify the YAML in this repo**
   
   Modify `tracked_workflows.yaml` to customize the [LF dashboard](https://olivialynn.github.io/lf-workflow-dash/). Add or remove repositories and workflows as needed. The format to follow is:

     ```yaml
     - repo: REPO_NAME
       owner: OWNER_NAME
       workflows:
         - WORKFLOW_NAME_1
         - WORKFLOW_NAME_2
         # Add more workflows if necessary
     ```
   The workflow name should be the entire file name, including the ".yml" or "yaml" ending.

3. **Or, submit an Issue**

   If you'd like to suggest changes or need assistance with modifying the YAML, feel free to open an issue in this repository. We'll be happy to help!

## Make Your Own Dashboard

1. **Fork this Repository**
   
   Feel free to delete `rail.html` and `rail_tracked_workflows.yaml` right away.

2. **Modify Your Tracked Workflows**

   Follow the instructions in [Modify the LF Dashboard](https://github.com/OliviaLynn/lf-workflow-dash/tree/main#modify-the-lf-dashboard) to make changes to your `tracked_workflows.yaml` file. 

3. **Activate GitHub Actions**

   Fresh forks require manual activation of GitHub Actions. Visit the "Actions" tab in your repository and enable the workflows.

4. **Authorization**

   Make sure to replace the username and email used in the commit step of `.github/workflows/main.yml`!
     
   **GitHub builds:** Your personal access token will be automatically generated when running the workflow on GitHub.

   **Local builds:** To build the HTML locally, run the following command in your repository:

     ```shell
     python update_dashboard.py PERSONAL_ACCESS_TOKEN tracked_workflows.yaml index.html
     ```

   You can generate a personal access token following these [GitHub token generation steps](TODO_ADD_LINK).

   Feel free to replace `tracked_workflows.yaml` with whatever input yaml you'd like; likewise, replace `index.html` with your desired output path.

5. **Page Title, Favicon, and Footer**

   Remember to customize your `<title>` tag, your favicon, and the footer at the bottom of the page that links to the dashboard's repo.

   Note that these need to be changed in `update_dashboard.py`, as any changes made to an HTML file will be overwritten.

7. **GitHub Pages (Optional)**

   If you want to host your dashboard on GitHub Pages, you'll need to [set up your repository for GitHub Pages.](TODO_ADD_LINK)

   Alternatively, you can use the [GitHub HTML Preview Tool](https://htmlpreview.github.io/?) to see your HTML without hosting it yourself. 

   For example, here's [LF dashboard via GitHub HTML Preview](https://htmlpreview.github.io/?url=https://github.com/OliviaLynn/workflow-dash/blob/main/index.html).

9. **Timezones (Optional)**

   We specify timezones for both the commit message timestamp and the dashboard times. If you want a different timezone, update it in both `main.yml` and `update_dashboard.py`.



That's it! You're ready to start monitoring your GitHub Actions workflows with your very own version of the LF dashboard.



## Contributing

Contributions are welcome! 

If you have ideas for improvements or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/OliviaLynn/lf-workflow-dash/blob/main/LICENSE) file for details.
