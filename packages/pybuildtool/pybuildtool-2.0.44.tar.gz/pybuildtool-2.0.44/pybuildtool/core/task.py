"""
Base class for pybuildtools tools.

Options:

    * _source_excluded_ : list, None
                        : Pretend source files (*_in values) don't exist.

    * _source_basedir_ : str, None
                       : Create files in output dir, relative path to source
                       : base directory.

    * _source_grouped_ : bool, None
                       : Don't create separate tasks for every input files, have
                       : them as input files of a single task.
                       : Actually I'm not so sure what this does, something like
                       : have them all as arguments to shell command?

    * _noop_retcodes_ : list, None
                      : If Task.perform() returns these, pretend nothing
                      : happened.

    * _success_retcodes_ : list, None
                         : If Task.perform() returns these, pretend as if it
                         : returns 0 or a success.

    * _replace_patterns_ : list, None
                         : If the output is a directory, you can rename the
                         : output files based on the source files.
                         : This is a list of list.
                         : The list elements consist of two items: python regex
                         : and replacement.

    * _no_io_ : bool, False
              : This task doesn't need inputs or outputs.
              : Only works if written in build.yml.

"""
import os
from copy import deepcopy
from time import time
from uuid import uuid4
#-
import locket
import stringcase
from waflib.Task import Task as BaseTask # pylint:disable=import-error
#-
from ..misc.collections_utils import make_list
from ..misc.path import expand_resource
from .rule import token_to_filename

class Task(BaseTask):
    """Base class for the tool

    Tool is called task in waf
    """
    PRODUCES_OUTPUT = True
    NEEDS_INPUT = True

    args = None
    args_case = 'spinal'
    conf = None
    group = None
    file_in = None
    file_out = None
    name = None
    token_in = None
    token_out = None

    _id = None

    def __init__(self, group, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = uuid4().hex

        # Task's configuration can be declared higher in the build tree,
        # but it needs to be prefixed with its tool-name.
        # Tool-name however can only be defined by the tool's module by
        # observing predefined `__name__` variable, which value is the name
        # of the tool's module.
        if config:
            my_config = deepcopy(config)
            if self.name:
                name = self.name + '_'
                for key in config.keys():
                    if not key.startswith(name):
                        continue
                    task_conf = key[len(name):]
                    if task_conf in config:
                        continue
                    my_config[task_conf] = config[key]
        else:
            my_config = {}
        self.args = []
        self.conf = my_config
        self.group = group
        self.file_in = []
        self.file_out = []
        self.token_in = []
        self.token_out = []


    def prepare(self):
        """Let tools prepare command arguments
        """


    def prepare_shadow_jutsu(self):
        """For tools that don't produce output files, inject timestamp files
        """
        source_exclude = []
        for f in make_list(self.conf.get('_source_excluded_')):
            nodes = expand_resource(self.group, f)
            source_exclude += make_list(nodes)

        task_uid = self._id

        for node in self.inputs:
            path = node.abspath()
            if node.parent.name == '.tokens':
                self.token_in.append(path)
            elif getattr(node, 'is_virtual_in_' + task_uid, False):
                pass
            elif path in source_exclude:
                pass
            else:
                self.file_in.append(path)

        for node in self.outputs:
            path = node.abspath()
            if node.parent.name == '.tokens':
                self.token_out.append(path)
            elif getattr(node, 'is_virtual_out_' + task_uid, False):
                pass
            else:
                self.file_out.append(path)


    def finalize_shadow_jutsu(self, create_only=False):
        """For tools that don't produce output files, generate timestamp files
        """
        for filename in self.token_out:
            if create_only and os.path.exists(filename):
                continue
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError:
                pass
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(time()))


    def run(self):
        """Tool's main function
        """
        self.prepare_shadow_jutsu()

        if self.file_in:
            if not self.NEEDS_INPUT:
                self.bld.fatal(f"{self.name.capitalize()} needs no input, "
                        f"received {repr(self.file_in)}")
            elif type(self.NEEDS_INPUT) is int and \
                    len(self.file_in) != self.NEEDS_INPUT: # pylint:disable=unidiomatic-typecheck
                self.bld.fatal(f"{self.name.capitalize()} only need "
                        f"{self.NEEDS_INPUT} input, received {repr(self.file_in)}")
        elif self.NEEDS_INPUT:
            self.bld.fatal(f"{self.name.capitalize()} needs input")

        if self.file_out:
            if not self.PRODUCES_OUTPUT:
                self.bld.fatal(f"{self.name.capitalize()} produces no output, "
                        f"received {repr(self.file_out)}")
            elif type(self.PRODUCES_OUTPUT) is int and \
                    len(self.file_out) != self.PRODUCES_OUTPUT: # pylint:disable=unidiomatic-typecheck
                self.bld.fatal(f"{self.name.capitalize()} at most produces "
                        f"{self.PRODUCES_OUTPUT} output, "
                        f"received {repr(self.file_out)}")

        self.prepare()

        lock_filename = '%s.lck' % token_to_filename(self.group.get_name(), # pylint:disable=consider-using-f-string
                self.bld)
        try:
            with locket.lock_file(lock_filename, timeout=5):
                ret = self.perform()
        except locket.LockError:
            self.bld.to_log(f"Task {self.group.get_name()} has already started.\n")
            ret = -1

        create_only = False
        if ret in make_list(self.conf.get('_noop_retcodes_')):
            create_only = True
            ret = None
        elif ret in make_list(self.conf.get('_success_retcodes_')):
            ret = None
        if not ret:
            self.finalize_shadow_jutsu(create_only)
        return ret


    @classmethod
    def toolenv(cls):
        """Get generic environment variable name for binary path
        """
        return f'{cls.name.upper()}_BIN'


    @staticmethod
    def is_production():
        """Check if it is production environment
        """
        return os.environ.get('PROJECT_VARIANT_IS_PRODUCTION') == '1'


    def stringcase_arg(self, option):
        """Convert text case of two-dash argument name
        """
        return getattr(stringcase, self.args_case + 'case')(option)


    def _add_arg(self, option, value, sep):
        """Add argument with custom value separator
        """
        if sep == ' ':
            self.args.append(option)
            self.args.append(value)
        else:
            self.args.append(option + sep + value)


    def add_bool_args(self, *options):
        """Read tool options, two-dash argument added based on truthy value
        """
        for option in options:
            value = self.conf.get(option)
            if not value:
                continue

            option = '--' + self.stringcase_arg(option)
            self.args.append(option)


    def add_dict_args(self, *options, **kwargs):
        """Read tool options, join key value, convert to two-dash argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')
        key_val_sep = kwargs.get('key_val_sep', '=')

        for option in options:
            if option not in self.conf:
                continue

            for key, value in self.conf[option].items():
                value = value.format(**self.group.get_patterns())
                item = key + key_val_sep + value
                self._add_arg('--' + option, item, opt_val_sep)


    def add_int_args(self, *options, **kwargs):
        """Read tool options, validate int and convert to two-dash argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            try:
                value = int(self.conf.get(option))
            except (TypeError, ValueError):
                continue

            option = '--' + self.stringcase_arg(option)
            self._add_arg(option, str(value), opt_val_sep)


    def add_list_args_join(self, separator, *options, **kwargs):
        """Read tool options, join and convert to two-dash argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            values = make_list(self.conf.get(option))
            if not values:
                continue

            option = '--' + self.stringcase_arg(option)
            value = separator.join(x.format(**self.group.get_patterns())\
                    for x in values)

            self._add_arg(option, value, opt_val_sep)


    def add_list_args_multi(self, *options, **kwargs):
        """Read tool options and convert to multiple two-dash arguments
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            values = make_list(self.conf.get(option))
            if not values:
                continue

            option = '--' + self.stringcase_arg(option)
            for value in values:
                value = value.format(**self.group.get_patterns())

                self._add_arg(option, value, opt_val_sep)


    def add_path_args(self, *options, **kwargs):
        """Read tool options, expand path and convert to two-dash argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            value = self.conf.get(option)
            if value is None:
                continue

            option = '--' + self.stringcase_arg(option)
            value = expand_resource(self.group, value)
            self._add_arg(option, value, opt_val_sep)


    def add_path_list_args_join(self, separator, *options, **kwargs):
        """Read tool options, join and convert to two-dash command argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            values = make_list(self.conf.get(option))
            if not values:
                continue

            option = '--' + self.stringcase_arg(option)
            value = separator.join(expand_resource(self.group, x)\
                    for x in values)

            self._add_arg(option, value, opt_val_sep)


    def add_path_list_args_multi(self, *options, **kwargs):
        """Read tool options and convert to multiple two-dash command arguments
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            values = make_list(self.conf.get(option))
            if not values:
                continue

            option = '--' + self.stringcase_arg(option)
            for value in values:
                value = expand_resource(self.group, value)
                self._add_arg(option, value, opt_val_sep)


    def add_str_args(self, *options, **kwargs):
        """Read tool options and convert to two-dash command argument
        """
        opt_val_sep = kwargs.get('opt_val_sep', '=')

        for option in options:
            value = self.conf.get(option)
            if value is None:
                continue

            option = '--' + self.stringcase_arg(option)
            value = value.format(**self.group.get_patterns())
            self._add_arg(option, value, opt_val_sep)
