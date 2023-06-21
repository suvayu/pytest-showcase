---
title: What is there to gain by using `pytest`?
---

# History

-   PyPy test suite
    -   testing focused development, probably because it&rsquo;s an alternate
        implementation of CPython
    -   developed a `std` library for developers
        -   `std` -> `py`
    -   test suite factored out: `py.test` -> `pytest`


# How to write tests using `pytest`?

-   simple functions
    -   may group tests into classes
-   assertions
    -   assertion rewriting
    -   natural syntax


# How does a failure look like?

-   rich output
-   errors and failures


# Running

-   test selection by name: `-k`
-   builtin: `skip`, `skipif`, `xfail`
-   custom: `example`
    -   test selection: `-m`
    -   available inside fixtures


# Fixtures

-   default fixtures
    -   temporary path/directory
    -   temporary path factory
    -   stdout/stderr: `capsys`
    -   logging: `caplog`
-   scope
-   composable


# Parametrisation

-   parametrised tests: `pytest.mark.parametrize`
-   parametrisable fixtures: via `request.param`


# Testing error messages

-   context manager
-   i/o capture


# `conftest`

-   fixtures
-   test helpers
-   process custom marks
-   &#x2026;

ecosystem: extensive set of plugins


# Incremental upgrade path

<https://docs.pytest.org/en/stable/how-to/unittest.html>

