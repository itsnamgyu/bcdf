import sys
sys.path.append('..')

import subprocess

from load.lib import auto_decode


def execute(args, stdin='', timeout=1) -> dict:
    '''
    Pass stdin input to executable w/ args and get return code, stdout, stderr string
    '''
    with subprocess.Popen(args,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as p:
        try:
            stdout, stderr = p.communicate(input=stdin.encode(),
                                           timeout=timeout)
        except subprocess.TimeoutExpired as e:
            p.kill()
            stdout, stderr = p.communicate()

        return dict(
            returncode=p.returncode,
            stdout=auto_decode(stdout),
            stderr=auto_decode(stderr))
