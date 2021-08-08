import time
import pytest
import subprocess
from selenium import webdriver


@pytest.fixture
def expensive_operations(request):
    if "last_in_group" in list(request._pyfuncitem.keywords.keys()):
        request.addfinalizer(cleanup_manager)
    time.sleep(0.5)


def cleanup_manager():
    print("\nCleaning up after expensive operation tests\n")


class TestManager:
    def __init__(self, temporary_folder):
        self.temporary_folder = temporary_folder

    def create_file(self, filename, text=""):
        (self.temporary_folder / filename).write_text(text)

    def run_ls(self, argument=""):
        if argument == "":
            result = subprocess.run(
                ["ls", self.temporary_folder], stdout=subprocess.PIPE
            )
        else:
            result = subprocess.run(
                ["ls", argument, self.temporary_folder], stdout=subprocess.PIPE
            )

        return result.stdout.decode("UTF-8")


@pytest.fixture
def test_manager(tmp_path):
    return TestManager(tmp_path)


@pytest.fixture(scope="class")
def web_driver(request):
    driver = webdriver.Firefox()

    def stop_driver():
        driver.close()

    request.addfinalizer(stop_driver)
    return driver


@pytest.hookimpl()
def pytest_collection_modifyitems(items, config):
    items.sort(key=lambda test: "expensive_operations" in test.fixturenames)

    if items:
        items[-1].add_marker("last_in_group")
