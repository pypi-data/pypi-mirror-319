""" Copy files.
"""
from shutil import copyfile, Error
from pybuildtool import BaseTask
from pybuildtool.misc.resource import get_filehash

tool_name = __name__

class Task(BaseTask):
    """cp task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_noop_retcodes_': 666,
    }

    def perform(self):
        """main function of the task
        """
        try:
            source_hash = get_filehash(self.file_in[0])
            if source_hash and source_hash == get_filehash(self.file_out[0]):
                return 666
            copyfile(self.file_in[0], self.file_out[0])
            return 0
        except Error:
            self.bld.fatal('tried to copy file to itself')
        except IOError:
            self.bld.fatal('destination location cannot be written')
        return 1
