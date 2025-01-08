"""
Validate javascript files.

Options:

    * config_file      : str, None, jscs configuration file
    * esnext           : bool, False, attempts to parse esnext code
                        (currently es6)
    * esprima          : str, None, attempts to use a custom version of Eprima
    * colors           : bool, True, output with colors
    * preset           : str, None, preset config
    * verbose          : adds rule names to the error output
    * max_errors       : int, None, maximum number of errors to report
    * error_filter     : str, None, a module to filter errors
    * reporter         : str, None, error reporter, console - default, text,
                         checkstyle, junit, inline
                         also accepts relative or absolute path to custom
                         reporter

Requirements:

    * node.js
    * jscs
      to install, run `npm install --save-dev jscs`

"""
import os
#-
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """jscs task
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
        c = cfg.get('config_file', None)
        if c:
            cstr = bld.path.find_resource(c).abspath()
            args.append(f"--config='{cstr}'")

        c = cfg.get('esnext', False)
        if c:
            args.append('--esnext')

        c = cfg.get('esprima', None)
        if c:
            cstr = bld.path.find_resource(c).abspath()
            args.append(f"--esprima='{cstr}'")

        c = cfg.get('colors', True)
        if not c:
            args.append('--no-colors')

        c = cfg.get('preset', None)
        if c:
            args.append(f"--preset='{c}'")

        c = cfg.get('verbose', False)
        if c:
            args.append('--verbose')

        c = cfg.get('max_errors', 0)
        if c > 0:
            args.append(f"--max-errors='{c}'")

        c = cfg.get('error_filter', None)
        if c:
            args.append(f"--error-filter='{c}'")

        if cfg.get('reporter', None):
            args.append(f'--reporter={cfg["reporter"]}')


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
    bin_path = 'node_modules/jscs/bin/jscs'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
    else:
        conf.end_msg('not found', color='YELLOW')
        bin_path = conf.find_program('jscs')[0]
    conf.env[Task.toolenv()] = bin_path
