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
            ("VMI12_source_mini.dat", "vmi12", "242efa5661042854eb0dcf9d0789f8a255d87ad75964615536ed4f1cc9a27434"),
            ("VMI13_source_mini.dat", "vmi13", "994175f2d24e03dab7ff4f8d03c1534ef58144dd8399d26f66d5c3464a1a5a9a")
        ]:
            input = str(resources / input)
            runner = CliRunner()
            with runner.isolated_filesystem():
                res = runner.invoke(main, ("convert", input, "-i", fmt, "out.csv"))
                self.assertEqual(res.exit_code, 0)
                with open("out.csv", "rb") as f:
                    self.assertEqual(hash, hashlib.sha256(f.read()).hexdigest())
