import os
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
