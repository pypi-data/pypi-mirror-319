"""
create and edit fonts in many formats: OpenType, TrueType, AAT, PostScript,
Multiple Master, CID-Keyed, SVG and various bitmap formats

Requirements:

    * fontforge
      to install, run `apt-get install fontforge` (for example)

"""
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """woff2svg task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'\.woff$', '.svg'), (r'\.woff2$', '.svg'))
    }

    def prepare(self):
        """prepare command arguments
        """
        args = self.args
        args.append('-lang ff')
        args.append("-c 'Open($1); Generate($2)'")


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
    bin_path = conf.find_program('fontforge')[0]
    conf.env[Task.toolenv()] = bin_path
