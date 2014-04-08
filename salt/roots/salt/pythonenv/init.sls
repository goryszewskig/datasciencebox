include:
  - users

conda:
  cmd.run:
    - name: "wget http://repo.continuum.io/miniconda/Miniconda-3.3.0-Linux-x86_64.sh -q -O miniconda.sh && bash miniconda.sh -b -p /home/ubuntu/anaconda && rm miniconda.sh"
    - cwd: /home/ubuntu
    - user: ubuntu
    - onlyif: "test ! -d /home/ubuntu/anaconda"

base-env:
  conda.managed:
    - name: /home/ubuntu/anaconda/envs/base
    - conda: /home/ubuntu/anaconda/bin/conda
    - packages: ipython-notebook
    - requirements: /srv/salt/pythonenv/requirements.txt
    - user: ubuntu
    - require:
      - cmd: conda

append-path:
  file.append:
    - name: /home/ubuntu/.zshrc
    - text: "export PATH=/home/ubuntu/anaconda/envs/base/bin:$PATH"
    - user: ubuntu
    - require:
      - file: dot_zshrc
      - conda: base-env

# IPython Notebook

/home/ubuntu/notebooks:
  file.directory:
    - user: ubuntu
    - makedirs: True

/home/ubuntu/nbserver.pid:
  nbserver.running:
    - directory: /home/ubuntu/notebooks
    - env: /home/ubuntu/anaconda/envs/base
    - stdout: /home/ubuntu/stdout.log
    - stderr: /home/ubuntu/stderr.log
    - user: ubuntu
    - require:
      - conda: base-env
