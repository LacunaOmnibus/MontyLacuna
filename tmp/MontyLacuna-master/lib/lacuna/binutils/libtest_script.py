
import lacuna.binutils.libbin
import argparse, lacuna, logging, os, sys

class TestScript(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = "This is just a test script to verify that MontyLacuna was installed properly.",
            epilog      = "EXAMPLE: python bin/test_script.py",
        )
        ### The test script is displaying empire profile, which requires the 
        ### real, not sitter, password.
        super().__init__(parser, 'real')

        ### This simple test script doesn't allow a --quiet arg.  The min log 
        ### level always gets set to INFO.
        self.client.user_log_stream_handler.setLevel(logging.INFO)

