"""
Browserify lets you require('modules') in the browser by bundling up all of
your dependencies.

This tool will accept multiple file_in, but only the first one will be
processed, the others are treated as dependency.

Options:

    * transform_module: list, [], use a transform module on
                        top-level files

Requirements:

    * node.js
    * browserify
      to install, run `npm install --save-dev browserify`

"""
import os
#-
from pybuildtool import BaseTask, make_list

tool_name = __name__

class Task(BaseTask):
    """browserify task
    """
    PRODUCES_OUTPUT = 1

    name = tool_name
    conf = {
        '_source_grouped_': True,
    }

    def prepare(self):
        """prepare command arguments
        """
        args = self.args
        conf = self.conf

        for mod in make_list(conf.get('transform_module')):
            args.append(f"--transform '{mod}'")


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} {in_} -o {out}')


def configure(conf):
    """waf configure
    """
    bin_path = 'node_modules/browserify/bin/cmd.js'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
    else:
        conf.end_msg('not found', color='YELLOW')
        bin_path = conf.find_program('browserify')[0]
    conf.env[Task.toolenv()] = bin_path
