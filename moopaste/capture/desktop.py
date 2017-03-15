
import re
from subprocess import check_output

WMNAME_EXPRS = (
    r'\(\s*(?P<name>[\w/_.-]+\.[\w/]{2,4})\s*\)',
    r'\[\s*(?P<name>[\w/_.-]+\.[\w/]{2,4})\s*\]',
    r'(?P<name>[\w/_]+\.[\w/]{2,4})',
)


class ActiveWindow(object):
    """Information about the active/focused window.
    """
    def __init__(self):
        self.window_id = None
        self.detect()

    def detect(self):
        """Find the active window via xprop.
        """
        active_window = check_output(('xprop', '-root', '_NET_ACTIVE_WINDOW'))
        self.window_id = active_window.split(' ')[-1]

    def get_title(self):
        """Gets the title of the active window
        """
        wmname_info = check_output(('xprop', '-id', self.window_id, 'WM_NAME'))
        # TODO: prune
        return wmname_info


def active_filenames():
    """Iterates through potential filenames that are in the active window.
    """
    win = ActiveWindow()
    title = win.get_title()
    for expr in WMNAME_EXPRS:
        match = re.search(expr, title)
        if match is not None:
            yield match.group('name')
    yield None
