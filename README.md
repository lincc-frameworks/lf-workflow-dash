<img src="https://github.com/lincc-frameworks/tape/blob/main/docs/DARK_Combo_sm.png?raw=true" width="300" height="100">


# LF Workflow Dash

[![view](https://img.shields.io/badge/view:-666666?style=for-the-badge)](#)
[![link-to-dash](https://img.shields.io/badge/LF_Dashboard-7b6db0?style=for-the-badge)](https://lincc-frameworks.github.io/lf-workflow-dash/)
[![link-to-rail-dash](https://img.shields.io/badge/RAIL_Dashboard-b08b3d?style=for-the-badge)](https://lincc-frameworks.github.io/lf-workflow-dash/rail.html)
[![link-to-rail-dash](https://img.shields.io/badge/Incubator_Dashboard-ECD53F?style=for-the-badge)](https://lincc-frameworks.github.io/lf-workflow-dash/incubator.html)

**LF Workflow Dash** is your easy solution for monitoring and managing GitHub Actions workflows. 

Track workflows across any number of repositories, check status and other relevant metrics, and quickly modify via yaml, all in one customizable dashboard.

Powered by the [GitHub REST API](https://docs.github.com/en/rest), **LF Workflow Dash** regularly retrieves data on specified GitHub Actions workflow runs and updates the dashboard HTML. This process is managed through scheduled GitHub workflows, and the output can be hosted easily using GitHub Pages.

## Getting Started

Click any of the badges at the top of the README to view a dashboard. 

Keep reading to learn about modifying an existing dashboard, or how to build your own dashboard.

## Modify the LF Dashboard

1. **Modify the YAML in this repo**
   
   Modify `config/tracked_workflows.yaml` to customize the [LF dashboard](https://lincc-frameworks.github.io/lf-workflow-dash/). Add or remove repositories and workflows as needed. The format to follow is:

   ```yaml
   repos:
      - repo: REPO_NAME
         owner: OWNER_NAME # github organization
         smoke-test: smoke-test.yml
         build-docs: build-documentation.yml
         benchmarks: asv-nightly.yml
         live-build: testing-and-coverage.yml
         other_workflows: 
         # Add more workflows if necessary
   ```

   We have columns for these 4 workflows, and the value should be the leaf yaml
   file name. If you have additional workflows, you can add them as `other_workflows`.

2. **Or, submit an Issue**

   If you'd like to suggest changes or need assistance with modifying the YAML, feel free to open an issue in this repository. We'll be happy to help!

## Make Your Own Dashboard

1. **Fork this Repository**
   
   Feel free to delete `rail.html` and `rail_tracked_workflows.yaml` right away.

2. **Modify Your Tracked Workflows**

   Follow the instructions in [Modify the LF Dashboard](https://github.com/lincc-frameworks/lf-workflow-dash/tree/main#modify-the-lf-dashboard) to make changes to your `tracked_workflows.yaml` file. 

3. **Activate GitHub Actions**

   Fresh forks require manual activation of GitHub Actions. Visit the "Actions" tab in your repository and enable the workflows.

   When enabled, the github workflow `.github/workflows/main.yml` will run every
   15 minutes to refresh the status of your dashboard.

4. **Authorization**

   **GitHub builds:** Your personal access token will be automatically generated when running the workflow on GitHub.

   **Local builds:** To build the HTML locally, run the following command in your repository:

     ```shell
     python update_dashboard.py PERSONAL_ACCESS_TOKEN tracked_workflows.yaml index.html
     ```

   You can generate a personal access token following these [GitHub token generation steps](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

   Feel free to replace `tracked_workflows.yaml` with whatever input yaml you'd like; likewise, replace `index.html` with your desired output path.

5. **Page Title, Favicon, and Footer**

   Remember to customize your `<title>` tag, your favicon, and the footer at the bottom of the page that links to the dashboard's repo.

   Note that these need to be changed in `templates/dash_template.jinja`, as any changes made to an HTML file will be overwritten.

7. **GitHub Pages (Optional)**

   If you want to host your dashboard on GitHub Pages, you'll need to [set up your repository for GitHub Pages.](https://docs.github.com/en/pages/quickstart)
   The github action for this repository will put the rendered HTML into a
   `gh-pages` branch, that should be used for hosting your Pages.

   Alternatively, you can use the [GitHub HTML Preview Tool](https://htmlpreview.github.io/?) to see your HTML without hosting it yourself. 

   For example, here's [LF dashboard via GitHub HTML Preview](https://htmlpreview.github.io/?https://github.com/lincc-frameworks/lf-workflow-dash/blob/main/index.html).

9. **Timezones (Optional)**

   We specify timezones for both the commit message timestamp and the dashboard times. If you want a different timezone, update it in both `main.yml` and `update_dashboard.py`.



That's it! You're ready to start monitoring your GitHub Actions workflows with your very own version of the LF dashboard.



## Contributing

Contributions are welcome! 

If you have ideas for improvements or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/lincc-frameworks/lf-workflow-dash/blob/main/LICENSE) file for details.
