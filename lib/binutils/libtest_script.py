
import binutils.libbin
import argparse, lacuna, os, sys

class TestScript(binutils.libbin.Script):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description = "This is just a test script to verify that MontyLacuna was installed properly.",
            epilog      = "EXAMPLE: python bin/test_script.py",
        )
        ### The test script is displaying empire profile, which requires the 
        ### real, not sitter, password.
        super().__init__(parser, 'real')

