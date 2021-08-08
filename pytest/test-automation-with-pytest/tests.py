import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):
    def expensive_operations(self):
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

    def test_list_multiple_files(self, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        test_manager.create_file("first.txt", "")
        test_manager.create_file("second.doc", "")
        result = test_manager.run_ls()
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with multiple files did not return expected result!"
        assert (
            "second.doc" in result
        ), "Listing a folder with multiple files did not return expected result!"

    def test_hidden_files(self, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        test_manager.create_file("first.txt", "")
        test_manager.create_file(".hidden_file", "")
        result = test_manager.run_ls()
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with hidden file did not return expected result!"
        assert (
            ".hidden_file" not in result
        ), "ls listed hidden file when it shouldn't have!"

    @pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Skipping non-windows test"
    )
    def test_list_hidden_files(self, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        test_manager.create_file("first.txt", "")
        test_manager.create_file(".hidden_file", "")
        result = test_manager.run_ls(argument="-a")
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with hidden file did not return expected result!"
        assert ".hidden_file" in result, "ls listed hidden file when it shouldn't have!"

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

    @pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
    def test_order(self, argument, test_manager):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        test_manager.create_file("first.txt")
        time.sleep(0.1)
        test_manager.create_file("second.txt")
        result = test_manager.run_ls(argument)
        assert result.startswith(
            "first.txt" if argument in ["", "-rt"] else "second.txt"
        ), "output of ls with argument '{}' was wrong!".format(argument)


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Skipping windows-only test"
)
class WindowsTest(object):
    @staticmethod
    @pytest.mark.notpassing
    def test_ls_windows():
        try:
            os.mkdir("c:\testfolder")
            Path("c:\testfolder\first.txt").touch()
            result = subprocess.run(["ls", "c:\testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with one file did not return expected result!"
        finally:
            shutil.rmtree("c:\testfolder")
