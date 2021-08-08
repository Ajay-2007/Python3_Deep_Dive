import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):
    @pytest.fixture
    def afixture(self):
        print("Afixture has run")
        return 42

    def expensive_operations(self):
        time.sleep(1)

    def test_list_empty_folder(self, tmp_path):
        """[summary]

        Returns:
            [type]: [description]
        """
        result = subprocess.run(["ls", str(tmp_path)], stdout=subprocess.PIPE)
        assert not result.stdout.decode(
            "UTF-8"
        ), "Listing an empty folder did not return expected result!"

    def test_simple_ls(self, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        Path(str(tmp_path) + "/first.txt").touch()
        result = subprocess.run(["ls", tmp_path], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with one file did not return expected result!"

    def test_list_multiple_files(self, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(str(tmp_path) + "/first.txt").touch()
        Path(str(tmp_path) + "/second.doc").touch()
        result = subprocess.run(["ls", str(tmp_path)], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with multiple files did not return expected result!"
        assert "second.doc" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with multiple files did not return expected result!"

    def test_hidden_files(self, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(str(tmp_path) + "/first.txt").touch()
        Path(str(tmp_path) + "/.hidden_file").touch()
        result = subprocess.run(["ls", str(tmp_path)], stdout=subprocess.PIPE)
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
    def test_list_hidden_files(self, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(str(tmp_path) + "/first.txt").touch()
        Path(str(tmp_path) + "/.hidden_file").touch()
        result = subprocess.run(["ls", "-a", str(tmp_path)], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with hidden file did not return expected result!"
        assert ".hidden_file" in result.stdout.decode(
            "UTF-8"
        ), "ls listed hidden file when it shouldn't have!"

    @pytest.mark.notpassing
    @pytest.mark.xfail(reason="-y parameter does not yet work")
    def test_unimplemented_feature(self, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        Path(str(tmp_path) + "/first.txt").touch()
        result = subprocess.run(["ls", "-y", str(tmp_path)], stdout=subprocess.PIPE)
        print("Result: [{}]".format(result))
        assert "first.txt" in result.stdout.decode(
            "UTF-8"
        ), "Listing a folder with -y option did not return expected result!"

    @pytest.mark.parametrize("argument", ["", "-r", "-t", "-rt"])
    def test_order(self, argument, tmp_path):
        """test simple ls

        Returns:
            [type]: [description]
        """
        self.expensive_operations()
        Path(str(tmp_path) + "/first.txt").touch()
        time.sleep(0.1)
        Path(str(tmp_path) + "/second.txt").touch()

        command = ["ls", argument, str(tmp_path)]
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
