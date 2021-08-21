import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_marker('timeout') is None:
            item.add_marker(pytest.mark.timeout(30))
