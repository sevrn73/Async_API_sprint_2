pytest_plugins = "functional.fixtures"

def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('asyncio')



