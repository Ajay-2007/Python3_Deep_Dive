import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):

    testfolder_path = "/tmp/testfolder_{}".format(
        str(os.environ.get("PYTEST_XDIST_WORKER"))
    )

    def expensive_operations(self):
        time.sleep(1)

    def setup(self):
        print("Setup")
        if not os.path.exists(self.testfolder_path):
            os.mkdir(self.testfolder_path)

    def teardown(self):
        if os.path.exists(self.testfolder_path):
            shutil.rmtree(self.testfolder_path)

    def test_list_empty_folder(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        result = subprocess.run(["ls", self.testfolder_path], stdout=subprocess.PIPE)
        assert not result.stdout.decode(
            "UTF-8"
        ), "Listing an empty folder did not return expected result!"

    def test_simple_ls(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        Path(self.testfolder_path + "/first.txt").touch()
        result = subprocess.run(["ls", self.testfolder_path], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with one file did not return expected result!"

    def test_list_multiple_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(self.testfolder_path + "/first.txt").touch()
        Path(self.testfolder_path + "/second.doc").touch()
        result = subprocess.run(["ls", self.testfolder_path], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with multiple files did not return expected result!"
        assert "second.doc" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with multiple files did not return expected result!"

    def test_hidden_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(self.testfolder_path + "/first.txt").touch()
        Path(self.testfolder_path + "/.hidden_file").touch()
        result = subprocess.run(["ls", self.testfolder_path], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with hidden file did not return expected result!"
        assert ".hidden_file" not in result.stdout.decode(
            "UTF-8"
        ), "ls listed hidden file when it shouldn't have!"

    @pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Skipping non-windows test"
    )
    def test_list_hidden_files(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(self.testfolder_path + "/first.txt").touch()
        Path(self.testfolder_path + "/.hidden_file").touch()
        result = subprocess.run(
            ["ls", "-a", self.testfolder_path], stdout=subprocess.PIPE
        )
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with hidden file did not return expected result!"
        assert ".hidden_file" in result.stdout.decode(
            "UTF-8"
        ), "ls listed hidden file when it shouldn't have!"

    @pytest.mark.notpassing
    @pytest.mark.xfail(reason="-y parameter does not yet work")
    def test_unimplemented_feature(self):
        """test simple ls

        Returns:
            [type]: [description]
        """
        Path(self.testfolder_path + "/first.txt").touch()
        result = subprocess.run(
            ["ls", "-y", self.testfolder_path], stdout=subprocess.PIPE
        )
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with -y option did not return expected result!"

    @pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
    def test_order(self, argument):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(self.testfolder_path + "/first.txt").touch()
        time.sleep(0.1)
        Path(self.testfolder_path + "/second.txt").touch()

        command = ["ls", argument, self.testfolder_path]
        arguments = " ".join(x for x in command if x != "")

        result = subprocess.run(shlex.split(arguments), stdout=subprocess.PIPE)
        assert result.stdout.decode("UTF-8").startswith(
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
