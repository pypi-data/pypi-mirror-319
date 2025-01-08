"""
Extract compressed files in a ZIP archive

Options:

    * extract_dir  : str, None,  destination directory (required)
    * quiet        : bool, False, quiet mode

Requirements:

    * unzip
      to install, for example run `apt-get install unzip`

"""
import os
#-
from pybuildtool import BaseTask, expand_resource

tool_name = __name__

class Task(BaseTask):
    """unzip task
    """
    PRODUCES_OUTPUT = False
    NEEDS_INPUT = 1

    name = tool_name

    def prepare(self):
        """prepare command arguments
        """
        # Update files, create if necessary
        self.args = ['-uo']

        c = self.conf.get('extract_dir')
        if c is None:
            self.bld.fatal('"extract_dir" configuration is required')

        path = c.format(**self.group.get_patterns())
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            os.remove(path)
            os.makedirs(path)
        self.args.append('-d ' + expand_resource(self.group, c))

        c = self.conf.get('quiet')
        if c:
            self.args.append('-q')


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        return self.exec_command(f'{exe} {arg} {in_}')


def configure(conf):
    """waf configure
    """
    bin_path = conf.find_program('unzip')[0]
    conf.env[Task.toolenv()] = bin_path
