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
            ("VMI12_source_mini.dat", "vmi12", "ea84cec6e7472f91121c60ea8e8c3083a79e179e874c197f103aeb94d5f59950"),
            ("VMI13_source_mini.dat", "vmi13", "9b43456e1c6fc236cde8ec2d7754f2bb0de02b78fa7f1630965cc30312a04150")
        ]:
            input = str(resources / input)
            runner = CliRunner()
            with runner.isolated_filesystem():
                res = runner.invoke(main, ("convert", input, "-i", fmt, "out.csv"))
                self.assertEqual(res.exit_code, 0)
                with open("out.csv", "rb") as f:
                    self.assertEqual(hash, hashlib.sha256(f.read()).hexdigest())
