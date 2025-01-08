""" Copy files.
"""
from shutil import copyfile, Error
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """copy task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name

    def perform(self):
        """main function of the task
        """
        try:
            copyfile(self.file_in[0], self.file_out[0])
            return 0
        except Error:
            self.bld.fatal('tried to copy file to itself')
        except IOError:
            self.bld.fatal('destination location cannot be written')
        return 1
