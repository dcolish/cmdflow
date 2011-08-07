from collections import namedtuple
from os import environ, unlink
from os.path import join as pjoin
from shlex import split
from subprocess import PIPE, Popen


class Path(object):
    """
    Provides some methods for building paths. A nice feature is the ability to
    combine additional `Path`s and/or strings to build a final path. Joining
    modifies the original `Path`. For example::

        Path("/usr/local") / "bin" / "foo"

    """
    def __init__(self, pathname):
        """
        Initialize a Path object::

            Path("/usr/local/")

        :param pathname: named path
        :type pathname: string
        """
        self.pathname = pathname

    def __repr__(self):
        return self.pathname

    def __div__(self, b):
        if isinstance(b, Path):
            self.pathname = pjoin(self.pathname, b.pathname)
            return self
        elif isinstance(b, str):
            self.pathname = pjoin(self.pathname, b)
        else:
            raise ValueError("Cannot join object into path")
        return self

    def unlink(self):
        """
        Remove the path from the Filesystem
        """
        unlink(self.pathname)


class ShellOutput(namedtuple("ShellOutput", "retcode stdout stderr")):
    """
    Manager of output from an executed cmdflow pipeline. Currently this can only
    redirect from the `ShellCmd`'s stdnout to a file.
    """

    def __gt__(self, b):
        """
        :param b: object to redirect stdout into
        """
        self.redirect('stdout', b)

    def redirect(self, path_out):
        """
        :param path_out: filesystem path to direct into
        """
        if isinstance(path_out, Path):
            path = path_out.pathname
        elif isinstance(path_out, str):
            path = path_out
        else:
            raise ValueError("Cannot redirect to this object")
        with open(path, 'w') as out:
            print >> out, self.stdout


class ShellCmd(object):
    """
    This is a wrapper on Popen to help make building pipelines of commands
    easier. The convenience syntax of '|' is reminiscent of regular shell
    semantics but it is a bit different. In this case you must explicitly call
    the resulting object
    """

    def __init__(self, cmd, env=None):
        """
        Initialize a ShellCmd::

            ShellCmd("echo 'hello'")

        :param cmds: commands to run
        :type cmd: list or string
        :param env: environment in which to run commands
        :type env: dict
        """
        if isinstance(cmd, str):
            cmd = split(cmd)
        assert all(True for word in cmd if 'sudo' == word)
        self.cmds = [cmd]
        if env == None:
            env = environ.copy()
        self.env = env

    def __call__(self, stdin=''):
        return self.run(stdin)

    def __gt__(self, b):
        if isinstance(b, str) or isinstance(b, Path):
            self() > b

    def __or__(self, b):
        return self.pipe(b)

    def __pos__(self):
        return SudoShellCmd(*self.cmds, env=self.env)

    def __repr__(self):
        return self().stdout

    def pipe(self, b):
        """
        Allows ShellCmd objects to feed input into each other in a style similar
        to shell pipelines

        :param b: command to append to ShellCmd.cmds
        :type b: ShellCmd
        """

        if isinstance(b, ShellCmd):
            b.cmds = self.cmds + b.cmds
            return b

    def run(self, stdin=()):
        """
        Being running `ShellCmd` pipeline

        :param stdin: Passed into stdin in `Popen`'s initializer
        :type stdin: str or ShellCmd
        :rtype: `ShellOutput`
        """
        first = True
        procs = []
        if isinstance(stdin, ShellCmd):
            self.cmds = stdin.cmds + self.cmds
            stdin = ''
        for cmd in self.cmds:
            if first:
                if stdin != '':
                    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                                 env=self.env)
                else:
                    proc = Popen(cmd, stdout=PIPE, stderr=PIPE,
                                 env=self.env)
                first = False
            else:
                proc = Popen(cmd, stdin=procs[-1].stdout,
                             stdout=PIPE, stderr=PIPE,
                             env=self.env)
            procs.append(proc)

        if len(procs) > 1:
            if stdin != '':
                procs[0].communicate(stdin)
            for proc in procs[:-1]:
                proc.stdout.close()
            stdout, stderr = procs[-1].communicate()
            retcode = procs[-1].returncode
        else:
            stdout, stderr = procs[0].communicate()
            retcode = procs[0].returncode

        return ShellOutput(retcode, stdout, stderr)


class SudoShellCmd(ShellCmd):
    """
    Class to represent allowed access to the `sudo` command or
    other escalated privileges.
    """

    def __init__(self, shell_cmd):
        super(SudoShellCmd, self).__init__(*self.cmds, env=self.env)
