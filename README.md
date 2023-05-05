# team02

## Getting Started


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