import time
import pytest
import subprocess


@pytest.fixture
def expensive_operations():
    time.sleep(1)


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
