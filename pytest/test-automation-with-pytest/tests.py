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

    @staticmethod
    def test_list_empty_folder():
        """[summary]

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            assert not result.stdout.decode(
                "UTF-8"
            ), "Listing an empty folder did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    def test_simple_ls():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with one file did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    def test_list_multiple_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/second.doc").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with multiple files did not return expected result!"
            assert "second.doc" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with multiple files did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    def test_hidden_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/.hidden_file").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with hidden file did not return expected result!"
            assert ".hidden_file" not in result.stdout.decode(
                "UTF-8"
            ), "ls listed hidden file when it shouldn't have!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Skipping non-windows test"
    )
    def test_list_hidden_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/.hidden_file").touch()
            result = subprocess.run(
                ["ls", "-a", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with hidden file did not return expected result!"
            assert ".hidden_file" in result.stdout.decode(
                "UTF-8"
            ), "ls listed hidden file when it shouldn't have!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    @pytest.mark.notpassing
    @pytest.mark.xfail(reason="-y parameter does not yet work")
    def test_unimplemented_feature():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            result = subprocess.run(
                ["ls", "-y", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            print("Result: [{}]".format(result))
            assert "first.txt" in result.stdout.decode(
                "UTF-8"
            ), "Listing a folder with -y option did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
    def test_order(self, argument):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            time.sleep(0.1)
            Path("/tmp/testfolder/second.txt").touch()

            command = ["ls", argument, "/tmp/testfolder"]
            arguments = " ".join(x for x in command if x != "")

            result = subprocess.run(shlex.split(arguments), stdout=subprocess.PIPE)
            assert result.stdout.decode("UTF-8").startswith(
                "first.txt" if argument in ["", "-rt"] else "second.txt"
            ), "output of ls with argument '{}' was wrong!".format(argument)

        finally:
            shutil.rmtree("/tmp/testfolder")


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
