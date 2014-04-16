# Bootstrap salt-cloud and its dependencies

python-pip:
  pkg.installed

curl:
  pkg.installed

salt-bootstrap:
    cmd.run:
      - name: "curl -L https://github.com/saltstack/salt-bootstrap/raw/stable/bootstrap-salt.sh | sudo sh -s -- git develop"
      - unless: "salt-cloud"
      - require:
        - pkg: curl

apache-libcloud:
  pip.installed:
    - require:
      - pkg: python-pip
