# Scholarship Applicant Review Utility
A web application built with streamlit to streamline the College of Engineering's committee which assigns scholarships to applicants.

**Note:** Many of the script commands you find throughout this README use the tool `poethepoet`, this can quickly be installed by running `pip install poethepoet`

## Running the Application
To run the full application experience (including launcher)
```
poe run
```

To run the streamlit server (headless)
```
poe run-server
```

## Developer Environment
We utilize the poetry package and dependency manager to handle building and installing libraries for our project. More information regarding Poetry can be found here: https://python-poetry.org/

### Building Distributables
Currently, building distributables is in an early state and is very unreliable. This method is not recommended currently, streamlit does not properly support this use case and our current adaptation uses several hacks in order to get it working. One of those hacks is that you must have the streamlit cli tool installed for your operating systems version of python. This can be installed with `pip install streamlit` inside your terminal.


Pyoxidizer will build both an executable and MacOS bundle which can be used to run the application as a more portable version of the codebase. Once the build process has completed the distributables will be found under dist/build
```sh
poe build
```
**Note:** Windows is not currently supported, only tested on MacOS

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

## Testing
### Flagging Specific Tests to Run
PyTest has the functionality to mark specific tests to run
```python
@pytest.mark.focus
def test_example():
```

These tests can be passed to our cli tool. If using the test.sh helper script found inside scripts/ you can do the following
```sh
sh scripts/test.sh "marker goes here"
```

The marker you add to the command will be passed to the `--focus` parameter of the cli tool which can also be run directly in a similar fashion.

```sh
python -m tests.cli --focus "marker goes here"
```

Currently markers only apply to the playwright specific tests will not carry over to the pyunit functional tests.