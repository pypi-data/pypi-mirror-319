"""
Manage runit services.

Options:

    * command  : str, None
               : service command to run, any of:
               : - start
               : - stop
               : - restart

    * target   : str, None
               : service directory to operate, can be wildcard

    * wait_sec : int, None
               : wait for status changes before exit

    * force    : bool, False
               : forceful execution of service command

Requirements:

    * runit
      to install, for example run `apt-get install runit`
"""
from subprocess import call
#-
from pybuildtool import BaseTask, expand_wildcard

tool_name = __name__

class Task(BaseTask):
    """runit_sv task
    """
    PRODUCES_OUTPUT = False
    NEEDS_INPUT = False

    name = tool_name

    targets = None

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        c = cfg.get('wait_sec', None)
        if c is not None:
            args.append(f'-w{c}')

        command = cfg.get('command', None)
        if command is None:
            self.bld.fatal('command option is required.')

        c = cfg.get('force', False)
        if c:
            args.append('force-' + command)
        else:
            args.append(command)

        target = cfg.get('target', None)
        if target:
            target = expand_wildcard(self.group, target, maxdepth=0)
        if not target:
            self.bld.fatal('target option is required.')
        self.targets = target


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        rets = []
        for target in self.targets:
            rets.append(call([exe] + self.args + [target]))
        return sum(abs(x) for x in rets)


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program('sv')[0]
