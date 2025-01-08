"""
Patch apply changes to a file

Options:

    * patch_file : str, None, location of patch file (can be made using this
                   command `diff -Naur original_file current_file` > patch_file

Requirements:

    * patch

"""
import os
#-
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """patch task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        if cfg.get('patch_file') is None:
            self.bld.fatal('InvalidOptions: "patch_file" is missing')
        args.append('-i ' + os.path.realpath(cfg['patch_file']))


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} -o {out} {in_}')


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program('patch')[0]
