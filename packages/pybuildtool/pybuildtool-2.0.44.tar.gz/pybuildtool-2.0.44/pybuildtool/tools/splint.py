"""
Splint is a tool for statically checking C programs for security vulnerabilites
and coding mistakes. With minimal effort, Splint can be used as a better lint.
If additional effort is invested adding annotations to programs, Splint can
perform stronger checking than can be done by any standard lint.

Options:

    * work_dir : str, None, Change current directory
    * flags    : list, [], enable or disable checks

Requirements:

    * splint
      to install, for example run `apt-get install splint`

"""
from pybuildtool import BaseTask, expand_resource, make_list

tool_name = __name__

class Task(BaseTask):
    """splint task
    """
    PRODUCES_OUTPUT = False

    name = tool_name

    workdir = None

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        # Change current directory, before running pylint, helps module imports
        c = cfg.get('work_dir')
        if c:
            self.workdir = expand_resource(self.group, c)
            if self.workdir is None:
                self.bld.fatal(cfg['work_dir'] + ' not found.')

        # Flags
        c = make_list(cfg.get('flags'))
        if not c:
            # see:
            # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=498809;msg=10
            c = [
                '-D__gnuc_va_list=va_list',
                '-warnposix',
                '+forcehints',
                '-formatcode',
                '-compdestroy',
            ]

        for flag in c:
            args.append(flag)


    def perform(self):
        """main function for the task
        """
        kwargs = {}
        if self.workdir is not None:
            kwargs['cwd'] = self.workdir

        exe = self.env[self.tool_env()]
        arg = ' '.join(self.args)
        in_ = ' '.join(self.file_in)
        return self.exec_command(f'{exe} {arg} {in_}', **kwargs)


def configure(conf):
    """waf configure
    """
    conf.env[Task.tool_env()] = conf.find_program(tool_name)[0]
