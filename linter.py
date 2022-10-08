# Copyright (c) 2013 Aparajita Fishman
# License: MIT
# Change for CudaLint: Alexey T.

import os
from cuda_lint import Linter, util
from cudax_nodejs import NODE_FILE

_js = os.path.join(os.path.dirname(__file__), 'node_modules', 'csslint', 'dist', 'cli.js')

class CSSLint(Linter):
    """Provides an interface to the csslint."""

    syntax = 'CSS'
    cmd = (NODE_FILE, _js, '--format=compact')
    regex = r'''(?xi)
        ^.+:\s*   # filename

        # csslint emits errors that pertain to the code as a whole,
        # in which case there is no line/col information, so that
        # part is optional.
        (?:line\ (?P<line>\d+),\ col\ (?P<col>\d+),\ )?
        (?:(?P<error>error)|(?P<warning>warning))\ -\ (?P<message>.*)
    '''
    word_re = r'^([#\.]?[-\w]+)'
    error_stream = util.STREAM_BOTH
    tempfile_suffix = 'css'
    defaults = {
        '--errors=,': '',
        '--warnings=,': '',
        '--ignore=,': ''
    }
    inline_overrides = ('errors', 'warnings', 'ignore')
    comment_re = r'\s*/\*'

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method so that general errors that do not have
        a line number can be placed at the beginning of the code.
        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if line is None and message:
            line = 0
            col = 0

        return match, line, col, error, warning, message, near
