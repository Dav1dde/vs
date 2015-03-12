import os
import os.path
import signal
import subprocess


def setup():
    root_path = os.path.dirname(__file__)
    config_path = os.path.join(root_path, 'redis.conf')
    pid_path = os.path.join(root_path, 'redis.pid')

    result = subprocess.Popen([
        'redis-server',
        config_path
    ], cwd=root_path, stdout=subprocess.PIPE)

    with open(pid_path, 'w') as fout:
        fout.write(str(result.pid))


def teardown():
    root_path = os.path.dirname(__file__)
    pid_path = os.path.join(root_path, 'redis.pid')

    with open(pid_path, 'r') as fin:
        pid = int(fin.read())

        os.kill(pid, signal.SIGTERM)
