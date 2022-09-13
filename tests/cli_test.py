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
            ("VMI12_source_mini.dat", "vmi12", "542938a36f569625eacb5c4e565772e646d41606a4761fb1a4288cde385e7e08"),
            ("VMI13_source_mini.dat", "vmi13", "e35cef1adaef0008a30f751adb8629d6a3c25d6850dfa90f1134331707254229")
        ]:
            input = str(resources / input)
            runner = CliRunner()
            with runner.isolated_filesystem():
                res = runner.invoke(main, ("convert", input, "-i", fmt, "out.csv"))
                self.assertEqual(res.exit_code, 0)
                with open("out.csv", "rb") as f:
                    self.assertEqual(hash, hashlib.sha256(f.read()).hexdigest())
