Done with ```pytest```

Unit tests should be descriptive, and cover:
- at least 1 common passing scenario FOR EACH kind of success
- at least 1 common failing scenario FOR EACH kind of failure
* *optionally 1 rare failing scenario*

Things being tested should be on separate rows.

Unit tests to be made in files titled ```test_<file_tested>.py```, with functions/methods ```test_<thing>()```, and classes with test methods must start with `Test`. This is imperative as `pytest` test discovery is based on names. 

Test coverage target - 80%

## Test structure

A test file must first import `context`, a file which sets the workdir to be the same as that of `main.py`.
After that, for each tested function/method, a test class is created, containing test methods.
Unless a function can be tested with only one case, then a single func may be used.
A test function should test for one thing, and preferably have only one assertion.

## End-to-end tests
Done with ```requests```

End-to-end tests should be valid usage scenarios with all endpoints used at least once.

End-to-end tests should ALWAYS clean up the project, as if cleanly initialized.

End-to-end tests may or may not be part of pre-commit hooks.
