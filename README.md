# Scholarship Applicant Review Utility
A web application built with streamlit to streamline the College of Engineering's committee which assigns scholarships to applicants.

## Developer Environment
We utilize the poetry package and dependency manager to handle building and installing libraries for our project. More information regarding Poetry can be found here: https://python-poetry.org/

### poethepoet
[poethepoet](https://github.com/nat-n/poethepoet) is an extension of Poetry which adds additional functionality such as post and pre build steps, alongside integrating easy scripts (often referred to as tasks) which are equivalent to scripts found in package.json in the Node package manager.

We have several poe tasks which can be run once you install poethepoet with the following:
```sh
pip install poethepoet
```

After poe is installed, it can be used to the tasks defined in `pyproject.toml`. For example, to run the streamlit server directly you can run the command:
```sh
poe run
```
or as a general format:
```sh
poe {task name}
```