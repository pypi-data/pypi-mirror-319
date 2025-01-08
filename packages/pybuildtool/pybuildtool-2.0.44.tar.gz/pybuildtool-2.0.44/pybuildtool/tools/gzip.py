"""
gzip compress files.

Requirements:

    * gzip

"""
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """gzip task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'$', '.gz'),),
    }

    def prepare(self):
        """prepare command arguments
        """
        self.args = ['--stdout', '--best']


    def perform(self):
        """main function for the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} {in_} > {out}')


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program('gzip')[0]
