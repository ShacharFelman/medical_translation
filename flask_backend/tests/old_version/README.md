# Tests

Module for testing the project's back-end.


## Developer Notes

### Refactory
This time, when refactoring, remember to KEEP IT SIMPLE. 

- Some code duplication is present in the tests.

### Upgrades
From most useful to least useful.

- Add differentiation between test failure and error, so that fixing the code becomes simpler.
  - This may require changing the exception which are thrown into Ones which inherit from some custom type, then acting based on whether the thrown exception is of that type or not.
- Disable some (if not all) loggers in tests, and add a TestLogger which logs what should be displayed.


