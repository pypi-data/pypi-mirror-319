"""
lftp is sophisticated file transfer progam

Options:

    * username: str, None, use the user for authentication
    * password: str, None, use the password for authentication
    * host    : str, None, host name, URL or bookmark name
    * port    : int, None, use the port for connection

Requirements:

    * lftp
      to install, for example run `apt-get install lftp`

"""
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):
    """lftp task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

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

        # user and password
        u = cfg.get('username', None)
        if u:
            p = cfg.get('password', None)
            if p:
                authstr = f'{u},{p}'
            else:
                authstr = u
            args.append(f'-u {authstr}')

        # port
        c = cfg.get('port', None)
        if c:
            args.append(f'-p {c}')

        # host
        c = cfg.get('host', None)
        if c:
            self.hoststr = c
        else:
            self.bld.fatal(f'configuration "host" is required for {tool_name}')


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        hst = self.hoststr
        return self.exec_command(f"{exe} {arg} -e 'put {in_} -o {out}' {hst}")


def configure(conf):
    """waf configure
    """
    conf.env[Task.toolenv()] = conf.find_program('lftp')[0]
