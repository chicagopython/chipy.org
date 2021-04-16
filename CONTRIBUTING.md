# Contributing to Chipy.org

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to the Chicago Python User Group website, which are hosted in the [Chicago Python User Group Organization](https://github.com/chicagopython). These are guidelines, not rules. Use your best judgement, and feel free to propose changes to this document in a pull request (PR).

## Code of Conduct

This project and everyone participating in it is governed by the [Chipy Code of Conduct](https://www.chipy.org/pages/conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior [here](https://www.chipy.org/contact/).

## How Can I Contribute?

Unsure where to begin contributing? You can start by looking through issues tagged `difficulty: easy` on the [issues page](https://github.com/chicagopython/chipy.org/issues).

### Local Development

Chipy.org can be deployed and viewed locally. For instructions on how to do this, see [README.md](README.md).

### Pull Requests

Please follow these steps to make your first PR!

1. Fork this repository by clicking the fork button at the top of the page. This will create an instance of the entire repository in your own account.
2. Clone the repository fork to your machine to work with it locally. On the GitHub for your fork, click the clone button and copy the link. Then, run the following commands to clone the repo and move into it:
    ```
    $ git clone https://github.com/YOUR_USERNAME_HERE/chipy.org

    $ cd chipy.org
    ```
3. Create a new branch with a short, descriptive name of the changes you'll make:
    ```
    $ git checkout -b BRANCH_NAME
    ```
4. Make changes to the branch to fix the issue you selected
5. Chipy.org uses Pytest, Pylint, and Black to encourage good software development techniques. Before you commit and push your changes, run our test suite, linter, and formatter:
    ```
    $ make test

    $ make lint

    $ make format
    ```
6. If any of the commands above fail, make changes to your code to successfully pass the three comamnds above.
7. Once your changes pass the automated tests and formatters, add your changes to the branch and make a commit with a descriptive message:
    ```
    $ git add .

    $ git commit -m "Adding a new feature to Chipy.org"
    ```
8. Push your commit(s) to your repository fork:
    ```
    $ git push origin BRANCH_NAME
    ```
9. Create a pull request by going to your repository fork on GitHub and clicking "Compare & pull request)
10. Congratulations! You've made your very first pull request.