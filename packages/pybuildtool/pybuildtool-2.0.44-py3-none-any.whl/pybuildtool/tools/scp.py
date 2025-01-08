"""
scp is secure copy (remote file copy program)

Options:

    * username     : str, None, use the user for authentication
    * identify_file: str, None, use the ssh private key file for authentication
    * host         : str, None, host name, URL or bookmark name
    * port         : int, None, use the port for connection

Requirements:

    * scp
      to install, for example run `apt-get install openssh`

"""
from pybuildtool import BaseTask, expand_resource

tool_name = __name__

class Task(BaseTask):
    """scp task
    """
    PRODUCES_OUTPUT = False
    NEEDS_INPUT = False

    name = tool_name
    conf = {
        '_source_grouped_': True,
    }

    hoststr = None

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        # identity file
        c = cfg.get('identity_file', None)
        if c:
            cstr = expand_resource(self.group, c)
            args.append(f'-i {cstr}')

        # port
        c = cfg.get('port', None)
        if c:
            args.append(f'-P {c}')

        # host
        h = cfg.get('host', None)
        if h:
            u = cfg.get('username', None)
            if u:
                self.hoststr = f'{u}@{h}'
            else:
                self.hoststr = h
        else:
            self.bld.fatal(f'configuration "host" is required for {tool_name}')


    def perform(self):
        """main function for the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        hst = self.hoststr
        return self.exec_command(f'{exe} {arg} {in_} {hst}:{out}')


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program('scp')[0]
