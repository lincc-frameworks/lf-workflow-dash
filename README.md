![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OliviaLynn/lf-workflow-dash/ci.yml)
[![codecov](https://codecov.io/gh/OliviaLynn/lf-workflow-dash/branch/master/graph/badge.svg)](https://codecov.io/gh/OliviaLynn/lf-workflow-dash)

# LF Workflow Dashboard

**[View Dashboard](https://olivialynn.github.io/lf-workflow-dash/)**

The **LF Workflow Dashboard** is a Python script that uses the GitHub API (TODO link) to fetch information about GitHub Actions workflow runs and generates an HTML dashboard to display the data. 

This provides an quick way to monitor the status and performance of workflows across multiple GitHub repositories at once.

## Getting Started

This section will guide you through the steps to get started with monitoring your GitHub Actions workflows.

You can modify `tracked_workflows.yaml` in this repo if you want to make changes to the LF Dashboard, or you can fork this repo and build your own dashboard.

### Option 1: Modify the LF Dashboard

1. **Modify the YAML in This Repo**

   - Clone this repository to your local machine:

     ```shell
     git clone https://github.com/OliviaLynn/workflow-dash.git
     ```

   - Open the `tracked_workflows.yaml` file in the repository.

   - Modify the YAML file to customize your LF dashboard. Add or remove repositories and workflows as needed. The format to follow is:

     ```yaml
     - repo: REPO_NAME
       owner: OWNER_NAME
       workflows:
         - WORKFLOW_NAME_1
         - WORKFLOW_NAME_2
         # Add more workflows if necessary
     ```
        The workflow name should be the entire file name, including the ".yml" or "yaml" ending.
   - Save your changes.

2. **Or submit an Issue**

   If you'd like to suggest changes or need assistance with modifying the YAML, feel free to open an issue in this repository. We'll be happy to help!

### Option 2: Fork the Repo to Make Your Own Dashboard

1. **Fork this Repository**

   - Click the "Fork" button in the top-right corner of this repository to create your copy.

2. **Modify Your YAML**

   - In your forked repository, navigate to the `tracked_workflows.yaml` file.

   - Follow the same YAML format described above to customize your dashboard, then save your changes.

3. **Activate GitHub Actions**

   - Fresh forks require manual activation of GitHub Actions. Visit the "Actions" tab in your repository and enable the workflows.

4. **Authorization**

   - This script uses a GitHub personal access token for authentication. Replace the username and email used in the commit step of `.github/workflows/main.yml`.

   - To build the HTML locally, run the following command in your repository:

     ```shell
     python update.py PERSONAL_ACCESS_TOKEN
     ```

     You can generate a personal access token following these [GitHub token generation steps](TODO_ADD_LINK).

5. **Footer Link**
    - TODO

6. **GitHub Pages (Optional)**

   - If you want to host your dashboard on GitHub Pages, you'll need to [set up your repository for GitHub Pages.](TODO_ADD_LINK).

   - Alternatively, you can use the [GitHub HTML Preview Tool](https://htmlpreview.github.io/?) to see your HTML without hosting it yourself. 
      - For example, here's [LF Dashboard via GitHub HTML Preview](https://htmlpreview.github.io/?url=https://github.com/OliviaLynn/workflow-dash/blob/main/index.html).

7. **Timezones (Optional)**

   - We specify timezones for both the commit message timestamp and the dashboard times. If you want a different timezone, update it in both `main.yml` and `update.py`.


That's it! You're ready to start monitoring your GitHub Actions workflows with your very own version of the LF Workflow Dashboard.



## Contributing

Contributions are welcome! If you have ideas for improvements or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

TODO add
