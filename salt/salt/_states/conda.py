# -*- coding: utf-8 -*-
import os


def execcmd(cmd, user=None):
    return __salt__['cmd.run_all'](' '.join(cmd), runas=user)


def managed(name, env=None, packages=None, requirements=None, conda=None, pip=None, user=None):
    """
    Create and install python requirements in a conda enviroment
    pip is isntalled by default in the new enviroment

    env : None
        environment name or path where to put the new enviroment
        if None (default) will use the default conda environment (`~/anaconda/bin`)
    packages : None
        single packge or list of packages to install i.e. numpy, scipy=0.13.3, pandas
    requirements : None
        path to a `requirements.txt` file in the `pip freeze` format
    conda : None
        Location for the `conda` command
        if None it is asumed the `conda` cmd is in the PATH
    pip : None
        location of the `pip` cmd to default libraries not in the conda repo
        if None (default) it is asumed the `pip` cmd is in the PAT
    user
        The user under which to run the commands
    """
    ans = {}
    ans['name'] = name
    ans['changes'] = {}
    ans['comment'] = ''
    comments = []
    ans['result'] = True

    if conda is None:
        # Assume `conda` is on the PATH
        conda = 'conda'

    if env != None:
        if '/' in env:
            # env is a path
            cmd = [conda, 'create', '--yes', '-q', '-p', env, 'pip']
        else:
            cmd = [conda, 'create', '--yes', '-q', '-n', env, 'pip']

        ret = execcmd(cmd, user)
        if ret['retcode'] == 0:
            comments.append('Virtual enviroment [%s] created' % env)
            ans['changes'][env] = 'Virtual enviroment created'
        else:
            if ret['stderr'].startswith('Error: prefix already exists:'):
                comments.append('Virtual enviroment [%s] already exists' % env)
            else:
                # Another error
                ans['comment'] = ret['stderr']
                ans['result'] = False
                return ans

    if packages is not None:
        installation_ans = installed(packages, env, conda=conda, pip=pip, user=user)
        ans['result'] = ans['result'] and installation_ans['result']
        comments.append('From list [%s]' % installation_ans['comment'])
        ans['changes'].update(installation_ans['changes'])

    if requirements is not None:
        installation_ans = installed(requirements, env, conda=conda, pip=pip, user=user)
        ans['result'] = ans['result'] and installation_ans['result']
        comments.append('From file [%s]' % installation_ans['comment'])
        ans['changes'].update(installation_ans['changes'])

    ans['comment'] = ' - '.join(comments)
    return ans


def installed(name, env=None, conda=None, pip=None, user=None):
    """
    Installs a single package, list of packages or packages in a requirements.txt

    name
        name of the package or path to the requirements.txt
    env
        path or name to the enviroment
    conda : None
        Location for the `conda` command
        if None it is asumed the `conda` command is in the PATH
    """
    ans = {}
    ans['name'] = name
    ans['changes'] = {}
    ans['result'] = True

    if conda is None:
        # Assume `conda` is on the PATH
        conda = 'conda'

    packages = []
    if os.path.exists(name) or name.startswith('salt://'):
        if name.startswith('salt://'):
            lines = __salt__['cp.get_file_str'](name)
            lines = lines.split('\n')
        elif os.path.exists(name):
            # name is a file
            lines = open(name, mode='r').readlines()

        for line in lines:
            # TODO: remove inline comments, so they are possible
            line = line.strip()
            if line == '' or line.startswith('#'):
                # Empty line or comment, go to next line
                continue
            else:
                packages.append(line)
    else:
        # Is not a file is a single package or list of packages
        temp = name.split(',')
        for package in temp:
            packages.append(package.strip())

    # Install packages
    installed = 0
    failed = 0
    old = 0
    for i, package in enumerate(packages):
        ret = install(package, env=env, conda=conda, pip=pip, user=user)
        if ret == 'OK':
            ans['changes'][package] = 'installed'
            installed = installed + 1
        elif ret == 'OLD':
            old = old + 1
        else:
            failed = failed + 1

    comment = '{0} packages installed, {1} already in installed, {2} failed'
    ans['comment'] = comment.format(installed, old, failed)

    if failed != 0:
        ans['result'] = False

    return ans


def install(package, env=None, conda=None, pip=None, user=None):
    """
    Helper function to install a single package from conda or defaulting to pip

    Returns
    -------
        "OK", "OLD" OR "ERROR: message"
    """
    if conda is None:
        conda = 'conda'

    if env is None:
        conda_base_cmd = [conda, 'install', '--yes', '-q']
    else:
        if '/' in env:
            # env is a path
            conda_base_cmd = [conda, 'install', '--yes', '-q', '-p', env]
        else:
            conda_base_cmd = [conda, 'install', '--yes', '-q', '-n', env]

    pip_base_cmd = [pip, 'install', '-q']

    if package.startswith('git'):
        # If its a git repo install using pip
        cmd = pip_base_cmd + [package]
        ret = execcmd(cmd, user)
        if ret['retcode'] == 0:
            return 'OK'
        else:
            return 'ERROR: ' + ret['stderr']
    else:
        cmd = conda_base_cmd + [package]
        ret = execcmd(cmd, user)

        if ret['retcode'] == 0:
            if '# All requested packages already installed' in ret['stdout']:
                return 'OLD'
            else:
                return 'OK'
        else:
            if 'Error: No packages found matching:' in ret['stderr']:
                # Package not in conda try pypi
                cmd = pip_base_cmd + [package]
                ret = execcmd(cmd, user)

                if ret['retcode'] == 0:
                    return 'OK'
                else:
                    # Could not find using conda or pypi
                    return 'ERROR: Package %s not found on conda or pypi' % package
            else:
                # Another conda error
                return 'ERROR: ' + ret['stderr']

