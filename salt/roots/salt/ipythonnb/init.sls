include:
  - python

/home/ubuntu/notebooks:
  file.directory:
    - user: ubuntu
    - makedirs: True

/home/ubuntu/nbserver.pid:
  nbserver.running:
    - directory: /home/ubuntu/notebooks
    - env: /home/ubuntu/anaconda
    - stdout: /home/ubuntu/stdout.log
    - stderr: /home/ubuntu/stderr.log
    - force: True
    - user: ubuntu
    - require:
      - conda: base-env
