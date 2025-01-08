"""
convert existing TrueType/OpenType fonts to WOFF format (subject to
appropriate licensing)

Requirements:

    * sfnt2woff
      to install, download/compile from http://people.mozilla.org/~jkew/woff/

"""
import re
#-
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """ttf2woff task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'\.ttf$', '.woff'), (r'\.otf$', '.woff'))
    }

    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        ret = self.exec_command(f'{exe} {arg} {in_}')

        if ret == 0:
            # success exit code
            move_executable = self.env['MV_BIN']
            converted_file = self.file_in[0]
            for (pat, rep) in self.conf['_replace_patterns_']:
                converted_file = re.sub(pat, rep, converted_file)

            exe = move_executable
            in_ = converted_file
            out = self.file_out[0]
            ret = self.exec_command(f'{exe} {in_} {out}')

        return ret


def configure(conf):
    """waf configure
    """
    if not conf.env.MV_BIN:
        conf.env.MV_BIN = conf.find_program('mv')[0]

    bin_path = conf.find_program('sfnt2woff')[0]
    conf.env[Task.toolenv()] = bin_path
