import io
import os
import shutil
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from importlib import resources

from compareworkbooks import difference

from BASE_dzne import core

DUMMYFILENAME = "dummy.txt"
SEQDATAZIPFILENAME = "SeqData.zip"
ABASE_113_INFILENAME = "aBASE-113-input.xlsx"
ABASE_113_GOALFILENAME = "aBASE-113-goal.xlsm"
ABASE_113_OUTFILENAME = "aBASE-113-output.xlsm"
CBASE_113_INFILENAME = "cBASE-113-input.xlsx"
CBASE_113_GOALFILENAME = "cBASE-113-goal.xlsx"
CBASE_113_OUTFILENAME = "cBASE-113-output.xlsx"
FILENAMES = [
    ABASE_113_GOALFILENAME,
    ABASE_113_INFILENAME,
    CBASE_113_GOALFILENAME,
    CBASE_113_INFILENAME,
    SEQDATAZIPFILENAME,
]


class TestLegacy(unittest.TestCase):

    def test_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.tmp = tmp
            self.set_files()
            self.copy_files()
            self.unzip()
            self.run_cBASE_113()
            self.run_aBASE_113()

        self.assertTrue(True)

    def copy_files(self):
        for filename in FILENAMES:
            target = os.path.join(self.tmp, filename)
            with resources.path("BASE_dzne.core.legacy.tests", filename) as source:
                shutil.copy(source, target)

    def run_aBASE_113(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            core.legacy.aBASE.run(
                infile=self.abase_113_infile,
                outfile=self.abase_113_outfile,
                hchain="G4:G300",
                heavykeys="H3:W3",
                kchain="Y4:Y300",
                kappakeys="Z3:AM3",
                lchain="AO4:AO300",
                lambdakeys="AP3:BC3",
                dataprefix=self.dataprefix,
            )
        stdoutstr = stdout.getvalue()
        stdout.close()
        stderrstr = stderr.getvalue()
        stderr.close()

        report = difference.files(self.abase_113_goalfile, self.abase_113_outfile)
        self.assertEqual(report.strip(), "", report)
        report = difference.files(self.abase_113_infile, self.abase_113_outfile)
        self.assertNotEqual(report.strip(), "", "aBASE: Infile equals outfile")
        report = difference.files(self.abase_113_infile, self.abase_113_goalfile)
        self.assertNotEqual(report.strip(), "", "aBASE: Infile equals goalfile")

    def run_cBASE_113(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            core.legacy.cBASE.run(
                infile=self.cbase_113_infile,
                outfile=self.cbase_113_outfile,
                dataprefix=self.dataprefix,
                pcr2read="A02:A177",
                plasmidread="B",
                shmanalysis="C",
            )
        stdoutstr = stdout.getvalue()
        stdout.close()
        stderrstr = stderr.getvalue()
        stderr.close()
        report = difference.files(
            self.cbase_113_goalfile, self.cbase_113_outfile, values=False
        )
        self.assertEqual(report.strip(), "", report)
        report = difference.files(
            self.cbase_113_infile, self.cbase_113_outfile, values=False
        )
        self.assertNotEqual(report.strip(), "", "cBASE: Infile equals outfile")
        report = difference.files(
            self.cbase_113_infile, self.cbase_113_goalfile, values=False
        )
        self.assertNotEqual(report.strip(), "", "cBASE: Infile equals goalfile")

    def set_files(self):
        self.seqdatazipfile = os.path.join(self.tmp, SEQDATAZIPFILENAME)
        self.dummyfile = os.path.join(self.tmp, "SeqData", DUMMYFILENAME)
        self.dataprefix = str(self.dummyfile)[: -len(DUMMYFILENAME)]
        self.cbase_113_infile = os.path.join(self.tmp, CBASE_113_INFILENAME)
        self.cbase_113_goalfile = os.path.join(self.tmp, CBASE_113_GOALFILENAME)
        self.cbase_113_outfile = os.path.join(self.tmp, CBASE_113_OUTFILENAME)
        self.abase_113_infile = os.path.join(self.tmp, ABASE_113_INFILENAME)
        self.abase_113_goalfile = os.path.join(self.tmp, ABASE_113_GOALFILENAME)
        self.abase_113_outfile = os.path.join(self.tmp, ABASE_113_OUTFILENAME)

    def unzip(self):
        with zipfile.ZipFile(self.seqdatazipfile, "r") as ref:
            ref.extractall(self.tmp)


if __name__ == "__main__":
    unittest.main()
