import os
import sys
import time
import shlex
import shutil
import pytest
import subprocess
from pathlib import Path


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
