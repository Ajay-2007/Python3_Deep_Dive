import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):
    def test_list_multiple_files(self, test_manager, expensive_operations):
        """test simple ls

        Returns:
            [type]: [description]
        """
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

    def test_hidden_files(self, test_manager, expensive_operations):
        """test simple ls

        Returns:
            [type]: [description]
        """
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
    def test_list_hidden_files(self, test_manager, expensive_operations):
        """test simple ls

        Returns:
            [type]: [description]
        """
        test_manager.create_file("first.txt", "")
        test_manager.create_file(".hidden_file", "")
        result = test_manager.run_ls(argument="-a")
        print("Result: [{}]".format(result))
        assert (
            "first.txt" in result
        ), "Listing a folder with hidden file did not return expected result!"
        assert ".hidden_file" in result, "ls listed hidden file when it shouldn't have!"

    @pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
    def test_order(self, argument, test_manager, expensive_operations):
        """test simple ls

        Returns:
            [type]: [description]
        """
        test_manager.create_file("first.txt")
        time.sleep(0.1)
        test_manager.create_file("second.txt")
        result = test_manager.run_ls(argument)
        assert result.startswith(
            "first.txt" if argument in ["", "-rt"] else "second.txt"
        ), "output of ls with argument '{}' was wrong!".format(argument)

