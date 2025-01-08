# gh-actions-deliver-python-package

Custom GitHub Action to deliver a python package to a pypi repository ([test.]pypi.org, or pypi.uoregon.edu).

## GitHub Self-Hosted Runner Requirements

- python (3.11 default)
- [twine](https://pypi.org/project/twine/)
- [build](https://pypi.org/project/build/)

## What is pypi.uoregon.edu?

Our Systems Automation Services team maintains a private Python Package Index (PyPI) service.

* Service URL https://pypi.uoregon.edu

> How to install packages from pypi.uoregon.edu:
> 
> * `pip install --extra-index-url https://pypi.uoregon.edu <your_package_name>`

### How-to: Deploy to pypi.uoregon.edu

1. Before publishing a new package to pypi.uoregon.edu, you need to follow instructions to create a 'service account' and an SSK Key Pair which will be the authentication solution used for the service account outlined in [Deploy to pypi.uoregon.edu (confluence)](https://confluence.uoregon.edu/x/ag5aGw).

2. You must provide a GitHub Secret that is an SSH Private Key which has permissions SSH Key or [API Token](https://test.pypi.org/help/#apitoken).

## Examples

### Example: How to Publish to pypi.org

1. Log in to your pypi.org account
2. Generate an [API Token](https://pypi.org/help/#apitoken).
3. Save as "PYPI_API_TOKEN" in your GitHub Repository.
4. Copy the following GitHub Workflow to "./github/workflows/test-and-deliver.yml":

```

```

# Appendix


# Development

Notes for future developers to maintain this solution.

## 'package-for-testing-gh-actions'

To test if this is a useful python package on this project, first set up a 'virtual environment' ('.venv):

```bash
python3 -m venv .venv && source .venv/bin/activate
```

Then install the package in editable mode

```
pip install -e .
```