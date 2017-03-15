
from subprocess import check_output
import tempfile


def get_selection(mode):
    """Gets a selection using xclip
    """
    return check_output(('xclip', '-o', '-selection', mode, '-'))


class SelectionFile(object):
    """Represents a file on disk with the supplied contents.

    file:// protocol files are returned as is.
    """
    def __init__(self, contents):
        self.name = None
        self.delete = False
        self.load(contents)

    def load(self, contents):
        """Ensures contents have a writable file on disk.
        """
        if contents.startswith('file:///'):
            self.name = contents[6:]
        else:
            outfile = tempfile.NamedTemporaryFile(delete=False)
            self.name = outfile.name
            self.delete = True
            outfile.write(contents)


def clipboard_file():
    """Gets a file with the contents of the CTRL+C clipboard.
    """
    contents = get_selection('clipboard')
    return SelectionFile(contents)


def paste_file():
    """Gets a file with the contents of the highlit buffer.
    """
    contents = get_selection('primary')
    return SelectionFile(contents)
