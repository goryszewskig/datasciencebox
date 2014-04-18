# -*- coding: utf-8 -*-
import os

def running(name, pid, stdout, stderr, cwd=None, force=False, user=None):
    ans = {}
    ans['name'] = name
    ans['changes'] = {}
    ans['result'] = True
    ans['comment'] = ''

    if os.path.exists(pid):
        f = open(pid, 'r')
        oldpid = f.read().strip()
        f.close()

        if force:
            # Kill process on that pid
            cmd = 'kill {pid} && rm {pidfile}'.format(pid=oldpid, pidfile=pid)
            __salt__['cmd.run_all'](cmd, runas=user)
            ans['changes']['old'] = 'Killed process %s' % oldpid
        else:
            ans['comment'] = 'Process is already running with pid: %s' % oldpid
            return ans

    cmd = '{cmd} >> {stdout} 2>> {stderr} &'
    cmd = cmd.format(cmd=name, stdout=stdout, stderr=stderr)
    dic = __salt__['cmd.run_all'](cmd, cwd=cwd, runas=user)
    newpid = dic['pid'] + 1

    # write pid filei
    cmd = "echo {pid} > {pidfile}".format(pid=newpid, pidfile=pid)
    __salt__['cmd.run_all'](cmd, runas=user)

    ans['comment'] = 'New background process running with pid {0}'.format(newpid)
    ans['changes']['new'] = 'New background process running with pid {0}'.format(newpid)

    return ans