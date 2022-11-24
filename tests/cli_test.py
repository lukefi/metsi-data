import unittest
import hashlib
import pathlib
import click
from forestdatamodel.cli import conv_inputfmt, conv_outputfmt, main
from click.testing import CliRunner

resources = pathlib.Path(__file__).resolve().parent / "resources"

class TestCli(unittest.TestCase):

    def test_inputformat(self):
        self.assertEqual(conv_inputfmt("input.xml"), "forest_centre")
        self.assertEqual(conv_inputfmt("input.pickle"), "pickle")
        with self.assertRaises(click.ClickException, msg="Can't infer input format"):
            conv_inputfmt("input.dat")

    def test_outputformat(self):
        self.assertEqual(conv_outputfmt("output.pickle"), "pickle")
        with self.assertRaises(click.ClickException, msg="Can't infer output format"):
            conv_outputfmt("output.dat")

    def test_run_convert_vmidata(self):
        for input, fmt, hash in [
            ("VMI12_source_mini.dat", "vmi12", "9ade47f5ac444eafb3256cb8ca180ad8b691eb1910bb750dd3644de35adc0114"),
            ("VMI13_source_mini.dat", "vmi13", "c40181c3b322db70c8c709d703d772457c1949f782387d887e7dea3c9e913bbf")
        ]:
            input = str(resources / input)
            runner = CliRunner()
            with runner.isolated_filesystem():
                res = runner.invoke(main, ("convert", input, "-i", fmt, "out.csv"))
                self.assertEqual(res.exit_code, 0)
                with open("out.csv", "rb") as f:
                    self.assertEqual(hash, hashlib.sha256(f.read()).hexdigest())
