include:
  - users

anaconda:
  cmd.run:
    - name: "wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-1.9.1-Linux-x86_64.sh -q -O anaconda.sh && bash anaconda.sh -b -p /home/ubuntu/anaconda && rm anaconda.sh"
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
