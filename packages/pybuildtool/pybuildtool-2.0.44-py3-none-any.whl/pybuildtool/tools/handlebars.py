"""
Precompile handlebars templates.

Options:

    * amd          : bool, None, exports amd style (require.js)
    * commonjs     : bool, None, exports CommonJS style, path to Handlebars
                     module [default: null]
    * handlebarpath: str, None, path to handlebar.js (only valid for amd-style)
                     [default: ""]
    * known        : list, [], known helpers
    * knownOnly    : bool, None, known helpers only
    * minimize     : bool, None, minimize output
    * namespace    : str, None, template namespace
                     [default: 'Handlebars.templates']
    * simple       : bool, None, output template function only
    * root         : str, None, template root, base value that will be stripped
                     from template names
    * partial      : bool, None, compiling a partial template
    * data         : hash, None, include data when compiling
    * extension    : str, None, template extension [default: 'handlebars']
    * bom          : bool, None, removes the BOM (Byte Order Mark) from the
                     beginning of the templates

Requirements:

    * handlebars
      to install, edit package.json, run `npm install`
    * node.js

"""
from json import dumps as json_dump
import os
#-
from pybuildtool import BaseTask, make_list

tool_name = __name__

class Task(BaseTask):
    """handlebars task
    """
    PRODUCES_OUTPUT = 1
    NEEDS_INPUT = 1

    name = tool_name
    conf = {
        '_replace_patterns_': ((r'\.handlebars$', '.js'),),
    }

    def prepare(self):
        """prepare command arguments
        """
        cfg = self.conf
        args = self.args

        c = cfg.get('amd')
        if c:
            args.append('--amd')

        c = cfg.get('commonjs')
        if c:
            args.append('--commonjs')

        c = cfg.get('handlebarpath')
        if c:
            args.append(f"--handlebarPath='{c}'")

        for handler in make_list(cfg.get('known')):
            args.append(f"--known='{handler}'")

        c = cfg.get('known_only')
        if c:
            args.append('--knownOnly')

        c = cfg.get('minimize')
        if c:
            args.append('--min')

        c = cfg.get('namespace')
        if c:
            args.append(f"--namespace='{c}'")

        c = cfg.get('simple')
        if c:
            args.append('--simple')

        c = cfg.get('root')
        if c:
            args.append(f"--root='{c}'")

        c = cfg.get('partial')
        if c:
            args.append('--partial')

        c = cfg.get('data')
        if c:
            args.append(f"--data='{json_dump(c)}'")

        c = cfg.get('extension')
        if c:
            args.append(f"--extension='{c}'")

        c = cfg.get('bom')
        if c:
            args.append('--bom')


    def perform(self):
        """main function of the task
        """
        exe = self.env[self.toolenv()]
        arg = ' '.join(self.args)
        in_ = self.file_in[0]
        out = self.file_out[0]
        return self.exec_command(f'{exe} {arg} {in_} -f {out}')


def configure(conf):
    """waf configure
    """
    bin_path = 'node_modules/handlebars/bin/handlebars'
    conf.start_msg(f"Checking for program '{tool_name}'")
    if os.path.exists(bin_path):
        bin_path = os.path.realpath(bin_path)
        conf.end_msg(bin_path)
    else:
        conf.end_msg('not found', color='YELLOW')
        bin_path = conf.find_program('handlebars')[0]
    conf.env[Task.toolenv()] = bin_path
