import os
import sys
import time
import shutil
import pytest
import subprocess
from pathlib import Path


class ClassTest(object):
    @staticmethod
    def test_list_empty_folder():
        """[summary]

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            assert (
                not result.stdout
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
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with one file did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    def test_list_multiple_files():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/second.doc").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with multiple files did not return expected result!"
            assert "second.doc" in str(
                result.stdout
            ), "Listing a folder with multiple files did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    def test_hidden_files():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/.hidden_file").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with hidden file did not return expected result!"
            assert ".hidden_file" not in str(
                result.stdout
            ), "ls listed hidden file when it shouldn't have!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    @pytest.mark.skipif(
        sys.platform.startswith("win"), reason="Skipping non-windows test"
    )
    def test_list_hidden_files():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            Path("/tmp/testfolder/.hidden_file").touch()
            result = subprocess.run(
                ["ls", "-a", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            print("Result: [{}]".format(result))
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with hidden file did not return expected result!"
            assert ".hidden_file" in str(
                result.stdout
            ), "ls listed hidden file when it shouldn't have!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    @pytest.mark.skipif(
        not sys.platform.startswith("win"), reason="Skipping windows-only test"
    )
    def test_ls_windows():
        try:
            os.mkdir("c:\testfolder")
            Path("c:\testfolder\first.txt").touch()
            result = subprocess.run(["ls", "c:\testfolder"], stdout=subprocess.PIPE)
            print("Result: [{}]".format(result))
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with one file did not return expected result!"
        finally:
            shutil.rmtree("c:\testfolder")

    @staticmethod
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
            assert "first.txt" in str(
                result.stdout
            ), "Listing a folder with -y option did not return expected result!"
        finally:
            shutil.rmtree("/tmp/testfolder")

    @staticmethod
    def test_order():
        """test simple ls

        Returns:
            [type]: [description]
        """
        try:
            os.mkdir("/tmp/testfolder")
            Path("/tmp/testfolder/first.txt").touch()
            time.sleep(0.1)
            Path("/tmp/testfolder/second.txt").touch()
            result = subprocess.run(["ls", "/tmp/testfolder"], stdout=subprocess.PIPE)
            assert result.stdout.decode("UTF-8").startswith(
                "first.txt"
            ), "output of ls with no arguments was wrong!"

            result = subprocess.run(
                ["ls", "-r", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            assert result.stdout.decode("UTF-8").startswith(
                "second.txt"
            ), "output of ls with -r argument was wrong!"

            result = subprocess.run(
                ["ls", "-t", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            assert result.stdout.decode("UTF-8").startswith(
                "second.txt"
            ), "output of ls with -t argument was wrong!"

            result = subprocess.run(
                ["ls", "-rt", "/tmp/testfolder"], stdout=subprocess.PIPE
            )
            assert result.stdout.decode("UTF-8").startswith(
                "first.txt"
            ), "output of ls with -rt argument was wrong!"

        finally:
            shutil.rmtree("/tmp/testfolder")
