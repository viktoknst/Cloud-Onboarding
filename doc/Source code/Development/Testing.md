### Unit tests
Done with ```pytest```

Unit tests should be descriptive, and cover:
- at least 1 common passing scenario FOR EACH kind of success
- at least 1 common failing scenario FOR EACH kind of failure
* *optionally 1 rare failing scenario*

Things being tested should be on separate rows.
Comments to be at most **5 words.**

Unit tests to be made in files titled ```test_<file_tested>.py```, with functions
```test_<func_tested>()```.

Unit tests to be added to pre-commit hooks.

Test coverage target - 80%

Code without a test is considered in development and not to be used.

### End-to-end tests
Done with ```requests```

End-to-end tests should be valid usage scenarios with all endpoints used at least once.

End-to-end tests should ALWAYS clean up the project, as if cleanly initialized.

End-to-end tests may or may not be part of pre-commit hooks.
