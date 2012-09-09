# -*- coding: utf-8 -*-
import os
import sys


class NodeScriptRunner(object):
    """docstring for NodeScriptRunner"""
    def __init__(self):
        super(NodeScriptRunner, self).__init__()

    def __getattr__(self, filename):
        def resolve_and_execute(filename, binary, dirnames):
            script_name = os.path.basename(filename)
            if script_name == 'node' or script_name == 'node.exe':
                script = [binary]
            else:
                for dirname in dirnames:
                    filename = os.path.join(dirname, script_name)
                    if os.path.isfile(filename):
                        if os.name is not 'nt':
                            script = [binary, filename]
                        else:
                            # On windows, npm wraps the script in a
                            # cmd executable, this means we can't
                            # change the version of node to run the
                            # script. So just run it with the default
                            # node.
                            script = [filename]
            args = script + sys.argv[1:]

            os.execve(args[0], args, os.environ)

        return resolve_and_execute.__get__(filename)


node_script_runner = NodeScriptRunner()
