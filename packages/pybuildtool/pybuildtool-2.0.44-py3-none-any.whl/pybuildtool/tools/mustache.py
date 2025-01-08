""" Render a mustache template with the given context.

Requirements:

    * pystache
      to install, run `pip install pystache`

"""
import os
#-
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """mustache task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name

    def perform(self):
        """main function of the task
        """
        # pylint:disable=import-outside-toplevel
        try:
            from chevron import render
        except ImportError:
            from pystache import render

        context = self.conf.get('context', {})
        os.makedirs(os.path.dirname(self.file_out[0]), exist_ok=True)
        with open(self.file_out[0], 'w', encoding='utf-8') as fout:
            with open(self.file_in[0], 'r', encoding='utf-8') as fin:
                fout.write(render(fin.read(), dict(context)))

        return 0
