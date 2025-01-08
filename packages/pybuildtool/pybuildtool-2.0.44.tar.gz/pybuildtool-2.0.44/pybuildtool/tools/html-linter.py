"""
HTML5 Linter based on Google Style Guide

Options:

    * disable : list:str, [], any combination of: doctype, entities,
                trailing_whitespace, tabs, charset, void_element,
                optional_tag, type_attribute, concerns_separation, protocol,
                names, capitalization, quotation, indentation, formatting,
                boolean_attribute, invalid_attribute, void_zero,
                invalid_handler, http_equiv, extra_whitespace

Requirements:

    * html-linter
      to install, run `pip install html-linter`

"""
from pybuildtool import BaseTask, make_list

tool_name = __name__

class Task(BaseTask):
    """html-linter task
    """
    name = tool_name
    conf = {
        '_source_grouped_': True,
    }

    disable_list = set(('doctype', 'entities', 'trailing_whitespace', 'tabs',
            'charset', 'void_element', 'optional_tag', 'type_attribute',
            'concerns_separation', 'protocol', 'names', 'capitalization',
            'quotation', 'indentation', 'formatting', 'boolean_attribute',
            'invalid_attribute', 'void_zero', 'invalid_handler', 'http_equiv',
            'extra_whitespace'))

    def prepare(self):
        """prepare command arguments
        """
        cfg = self. conf
        args = self.args

        c = make_list(cfg.get('disable'))
        if c:
            invalid_disable_items = set(c) - self.disable_list
            if invalid_disable_items:
                self.bld.fatal('invalid disable configuration items: ' +\
                        ', '.join(invalid_disable_items))
            args.append('--disable=' + ','.join(c))


    def perform(self):
        """main function for the task
        """
        exe = self.env[self.toolenv()]
        for file_in in self.file_in:
            arg = ' '.join(self.args)
            in_ = file_in
            return_code = self.exec_command(f'{exe} {arg} {in_}')

            if return_code:
                self.bld.fatal(f'Found syntax errors in {file_in}')
        return 0


def configure(conf):
    """waf configure
    """
    bin_path = conf.find_program('html_lint.py')[0]
    conf.env[Task.toolenv()] = bin_path
