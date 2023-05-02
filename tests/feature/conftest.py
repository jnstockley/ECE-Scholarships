'''
Pytest configuration file. Can store fixtures, hooks, and other configuration options.
'''
pytest_plugins = [
   "tests.feature.fixtures.import_data",
   "tests.feature.fixtures.login"
]
