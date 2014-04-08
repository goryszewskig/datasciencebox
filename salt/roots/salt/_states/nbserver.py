# -*- coding: utf-8 -*-
import os


def running(name, directory, env=None, ip='0.0.0.0', port=8888, force=False, stdout=None, stderr=None, user=None):
    '''
    name is the path with (to) the pid
    '''
    ans = {}
    ans['name'] = name
    ans['changes'] = {}
    ans['result'] = True
    ans['comment'] = ''

    if os.path.exists(name):
        f = open(name, 'r')
        pid = f.read().strip()
        f.close()

        if force:
            # Kill process on that pid
            cmd = 'kill {pid} && rm {pidfile}'.format(pid=pid, pidfile=name)
            __salt__['cmd.run_all'](cmd, runas=user)
            cmd = 'rm %s' % name
            __salt__['cmd.run_all'](cmd, runas=user)
            ans['changes']['old'] = 'Killed process (%s)' % pid
        else:
            ans['comment'] = 'Agent is already running with pid: %s' % pid
            return ans

    # Start notebook
    if env is None:
        ipython = 'ipython'
    else:
        ipython = os.path.join(env, 'bin', 'ipython')
    cmd = '{ipython} notebook --ip={ip} --port={port} --no-browser >> {stdout} 2>> {stderr} &'
    cmd = cmd.format(ipython=ipython, ip=ip, port=port, stdout=stdout, stderr=stderr)
    print '!!!!!!', cmd
    dic = __salt__['cmd.run_all'](cmd, cwd=directory, runas=user)
    pid = dic['pid']

    # write pid filei
    cmd = "echo {pid} > {pidfile}".format(pid=pid, pidfile=name)
    __salt__['cmd.run_all'](cmd, runas=user)

    ans['comment'] = 'New notebook running in {0}:{1} with pid {2}'.format(ip, port, pid)
    ans['changes']['new'] = 'New notebook running in {0}:{1} with pid {2}'.format(ip, port, pid)

    return ans