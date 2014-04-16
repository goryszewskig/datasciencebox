include:
  - users

anaconda:
  cmd.run:
    - name: "wget http://repo.continuum.io/miniconda/Miniconda3-3.3.0-Linux-x86_64.sh -q -O miniconda.sh && bash miniconda.sh -b -p /home/ubuntu/anaconda && rm miniconda.sh"
    - cwd: /home/ubuntu
    - user: ubuntu
    - onlyif: "test ! -d /home/ubuntu/anaconda"

base-env:
  conda.managed:
    - conda: /home/ubuntu/anaconda/bin/conda
    - pip: /home/ubuntu/anaconda/bin/pip
    - packages: ipython-notebook
    - requirements: /srv/salt/python/requirements.txt
    - user: ubuntu
    - require:
      - cmd: anaconda

append-path:
  file.append:
    - name: /home/ubuntu/.zshrc
    - text: "export PATH=/home/ubuntu/anaconda/bin:$PATH"
    - user: ubuntu
    - require:
      - file: dot_zshrc
      - conda: base-env
