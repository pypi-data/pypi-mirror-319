"""
Generate documentation.

Options:

    * work_dir      : str, None, change current directory
    * config_file   : str, None, doxygen configuration file

Requirements:

    * doxygen
      to install, for example run `apt-get install doxygen`

"""
from pybuildtool import BaseTask, expand_resource

tool_name = __name__

class Task(BaseTask):
    """doxygen task
    """
    PRODUCES_OUTPUT = False
    NEEDS_INPUT = False

    name = tool_name

    workdir = None

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        # Change current directory, before running pylint, helps module imports
        c = cfg.get('work_dir', None)
        if c:
            self.workdir = expand_resource(self.group, c)
            if self.workdir is None:
                self.bld.fatal(cfg['work_dir'] + ' not found.')

        # Specify a configuration file
        c = cfg.get('config_file', None)
        if c:
            args.append(expand_resource(self.group, c))


    def perform(self):
        """main function of the task
        """
        kwargs = {}
        if self.workdir is not None:
            kwargs['cwd'] = self.workdir

        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        return self.exec_command(f'{exe} {arg}', **kwargs)


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program(tool_name)[0]
