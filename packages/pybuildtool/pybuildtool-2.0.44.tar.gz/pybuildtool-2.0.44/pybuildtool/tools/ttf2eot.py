"""
very quick commandline wrapper around OpenTypeUtilities.cpp from Chromium,
used to make EOT (Embeddable Open Type) files from TTF (TrueType/OpenType
Font) files

Requirements:

    * ttf2eot
      to install, download/compile from https://github.com/metaflop/ttf2eot

"""
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """ttf2eot task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'\.ttf$', '.eot'), (r'\.otf$', '.eot'))
    }

    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} < {in_} > {out}', stdout=None)


def configure(conf):
    """waf configure
    """
    bin_path = conf.find_program('ttf2eot')[0]
    conf.env[Task.toolenv()] = bin_path
