import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):
    # @pytest.fixture
    # def expensive_operations(self):
    #     time.sleep(1)

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
    def test_manager(self, tmp_path):
        return self.TestManager(tmp_path)

    def test_list_empty_folder(self, test_manager):
        """[summary]

        Returns:
            [type]: [description]
        """
        assert (
            not test_manager.run_ls()
        ), "Listing an empty folder did not return expected result!"

    def test_simple_ls(self, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        test_manager.create_file("first.txt")
        result = test_manager.run_ls()
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with one file did not return expected result!"

    @pytest.mark.notpassing
    @pytest.mark.xfail(reason="-y parameter does not yet work")
    def test_unimplemented_feature(self, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        test_manager.create_file("first.text")
        test_manager.run_ls(argument="-y")
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with -y option did not return expected result!"
