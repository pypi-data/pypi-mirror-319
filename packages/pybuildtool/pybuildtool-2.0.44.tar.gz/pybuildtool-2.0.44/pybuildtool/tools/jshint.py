"""
Validate javascript files.

Options:

    * config_file      : str, None, jshint configuration file
    * reporter         : str, None, custom reporter
    * ignore_files     : list, [],  excludes files matching pattern
    * ignore_list_file : str, None, jshintignore file

Requirements:

    * node.js
    * jshint
      to install, run `node install --save-dev jshint`

"""
import os
#-
from pybuildtool import BaseTask, make_list

tool_name = __name__

class Task(BaseTask):
    """jshint task
    """
    name = tool_name
    conf = {
        '_source_grouped_': True,
    }

    def prepare(self):
        """prepare command arguments
        """
        bld = self.group.context
        cfg = self.conf
        args = self.args

        # Custom configuration file
        if cfg.get('config_file', None):
            config_file = bld.path.find_resource(cfg['config_file']).abspath()
            args.append(f"--config='{config_file}'")

        # Custom reporter (<PATH>|jslint|checkstyle)
        if cfg.get('reporter', None):
            args.append(f'--reporter={cfg["reporter"]}')

        # Exclude files matching the given filename pattern
        # (same as .jshintignore)
        exclude_files = make_list(cfg.get('ignore_files'))
        for exclude_file in exclude_files:
            args.append(f'--exclude={exclude_file}')

        # Pass in custom jshintignore file path
        if cfg.get('ignore_list_file', None):
            ignore_file = bld.path.find_resource(cfg['ignore_list_file']).abspath()
            args.append(f"--exclude-path='{ignore_file}'")


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = ' '.join(self.file_in)
        return self.exec_command(f'{exe} {arg} {in_}')


def configure(conf):
    """waf configure
    """
    bin_path = 'node_modules/jshint/bin/jshint'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
    else:
        conf.end_msg('not found', color='YELLOW')
        bin_path = conf.find_program('jshint')[0]
    conf.env[Task.toolenv()] = bin_path
