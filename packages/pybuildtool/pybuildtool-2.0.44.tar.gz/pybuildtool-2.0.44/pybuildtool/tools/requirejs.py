"""
A command line tool for running JavaScript scripts that use the AMD API for
declaring and using JavaScript modules and regular JavaScript script files.

Options:

    * work_dir     : str, None, change current directory before run
    * config_file  : str, None, r.js build file

Requirements:

    * node.js
    * requirejs
      to install, run `npm install --save-dev requirejs`

"""
import os
#-
from pybuildtool import BaseTask, expand_resource

tool_name = __name__

class Task(BaseTask):
    """requirejs task
    """
    name = tool_name

    prefix = []

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf

        # Change current directory
        c = cfg.get('work_dir', None)
        if c:
            cstr = expand_resource(self.group, c)
            self.prefix.append(f'cd {cstr};')

        config_file = expand_resource(self.group, cfg['config_file'])
        self.args.append(f'-o {config_file}')


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        pre = ' '.join(self.prefix)
        arg = ' '.join(self.args)
        return self.exec_command(f'{pre} {exe} {arg}')


def configure(conf):
    """waf configure
    """
    bin_path = 'node_modules/requirejs/bin/r.js'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
        conf.env[Task.toolenv()] = bin_path
    else:
        conf.end_msg('not found', color='YELLOW')
