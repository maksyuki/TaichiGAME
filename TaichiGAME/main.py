import sys
import shutil
import runpy
import argparse
import subprocess
from pathlib import Path
from typing import Dict

import colorama as cra


def registerableCLI(cls):
    """Class decorator to register methodss with @register into a set."""
    cls._registered_commands = set([])
    for name in dir(cls):
        method = getattr(cls, name)
        if hasattr(method, '_registered'):
            cls._registered_commands.add(name)
    return cls


def register(func):
    """Method decorator to register CLI commands."""
    func._registered = True
    return func


@registerableCLI
class TaichiGAMEMain():
    def __init__(self, test_mode: bool = False):
        cra.init()
        self._banner = cra.Fore.GREEN + f"\n{'#' * 70}\n"
        self._banner += '##  TaichiGAME: GPU Accelerated Motion Engine '
        self._banner += 'based on Taichi Lang  ##'
        self._banner += f"\n{'#' * 70}"
        print(self._banner)

        parser = argparse.ArgumentParser(description="TaichiGAME CLI",
                                         usage=self._usage())
        parser.add_argument('command',
                            help="command from the above list to run")

        # Flag for unit testing
        self._test_mode = test_mode
        self._main_parser = parser

    def _usage(self) -> str:
        """Compose deterministic usage message based on registered_commands."""
        # TODO: add some color to commands
        msg = "\n"
        space = 20
        for command in sorted(self._registered_commands):  # type: ignore # pylint: disable=E1101
            msg += f"    {command}{' ' * (space - len(command))}|-> {getattr(self, command).__doc__}\n"
        return msg

    @staticmethod
    def _exec_python_file(filename: str):
        """Execute a Python file based on filename."""
        # TODO: do we really need this?
        subprocess.call([sys.executable, filename] + sys.argv[1:])

    @staticmethod
    def _get_examples_dir() -> Path:
        """Get the path to the examples directory."""
        root_dir = '.'
        examples_dir = Path(root_dir) / 'examples'
        print('example dir: ####$#$#$', examples_dir)
        return examples_dir

    @staticmethod
    def _get_available_examples() -> Dict[str, Path]:
        """Get a set of all available example names."""
        examples_dir = TaichiGAMEMain._get_examples_dir()
        all_examples = examples_dir.rglob('*.py')
        all_example_names = {f.stem: f.parent for f in all_examples}
        return all_example_names

    @staticmethod
    def _example_choices_type(choices):
        def support_choice_with_dot_py(choice):
            if choice.endswith('.py') and choice.split('.')[0] in choices:
                # try to find and remove python file extension
                return choice.split('.')[0]
            return choice

        return support_choice_with_dot_py

    def __call__(self):
        # Print help if no command provided
        if len(sys.argv[1:2]) == 0:
            self._main_parser.print_help()
            return 1

        # Parse the command
        args = self._main_parser.parse_args(sys.argv[1:2])

        if args.command not in self._registered_commands:  # type: ignore # pylint: disable=E1101
            # TODO: do we really need this?
            if args.command.endswith(".py"):
                TaichiGAMEMain._exec_python_file(args.command)
            else:
                print(f"{args.command} is not a valid command!")
                self._main_parser.print_help()
            return 1

        return getattr(self, args.command)(sys.argv[2:])

    @register
    def example(self, arguments: list = sys.argv[2:]):
        """Run an example by name (or name.py)"""
        choices = TaichiGAMEMain._get_available_examples()

        parser = argparse.ArgumentParser(prog='python3 -m TaichiGAME example',
                                         description=f"{self.example.__doc__}")

        parser.add_argument(
            "name",
            help="Name of an example (supports .py extension too)\n",
            type=TaichiGAMEMain._example_choices_type(choices.keys()),
            choices=sorted(choices.keys()))
        parser.add_argument(
            '-p',
            '--print',
            required=False,
            dest='print',
            action='store_true',
            help="Print example source code instead of running it")
        parser.add_argument(
            '-P',
            '--pretty-print',
            required=False,
            dest='pretty_print',
            action='store_true',
            help="Like --print, but print in a rich format with line numbers")
        parser.add_argument(
            '-s',
            '--save',
            required=False,
            dest='save',
            action='store_true',
            help="Save source code to current directory instead of running it")

        # TODO: Pass the arguments to downstream correctly(#3216).
        args = parser.parse_args(arguments)
        examples_dir = TaichiGAMEMain._get_examples_dir()
        target = str(
            (examples_dir / choices[args.name] / f"{args.name}.py").resolve())
        # path for examples needs to be modified for implicit relative imports
        sys.path.append(str((examples_dir / choices[args.name]).resolve()))

        # Short circuit for testing
        if self._test_mode:
            return args

        if args.save:
            print(f"Saving example {args.name} to current directory...")
            shutil.copy(target, '.')
            return 0

        if args.pretty_print:
            return 0

        if args.print:
            with open(target, encoding='utf-8') as f:
                print(f.read())
            return 0

        print(f"Running example {args.name} ...")

        runpy.run_path(target, run_name='__main__')

        return None


def main():
    cli = TaichiGAMEMain()

    return cli()


if __name__ == '__main__':
    sys.exit(main())
