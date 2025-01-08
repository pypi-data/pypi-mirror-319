"""
Less-css is a CSS pre-processor, meaning that it extends the CSS language,
adding features that allow variabels, and mixins, functions and many other
techniques that allow you to make CSS that is more maintainable, themable and
extendable.

Options:

    * keep_line_breaks     : bool, False, keep line breaks

Requirements:

    * node.js
    * less
      to install, run `npm install --save-dev less`

"""
import os
#-
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """less task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'\.less$', '.css'),)
    }

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        # keep line breaks
        if cfg.get('keep_line_breaks', False):
            args.append('--keep-line-breaks')


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} {in_} {out}')


def configure(conf):
    """waf configure
    """
    bin_path = 'node_modules/less/bin/lessc'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
    else:
        conf.end_msg('not found', color='YELLOW')
        bin_path = conf.find_program('lessc')[0]
    conf.env[Task.toolenv()] = bin_path
