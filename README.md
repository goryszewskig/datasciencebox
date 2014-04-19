DataScienceBox
==============

My personal data science box based on [salt](http://www.saltstack.com/) and
[Vagrant](http://vagrantup.com/) to easily create cloud instances or local VMs
ready for doing data science.

Includes
--------

- Ubuntu 12.04
- Python 2.7.4 environment based on [Anaconda](http://continuum.io/downloads)
- [IPython notebook](http://ipython.org/notebook.html) running in port 8888
- [s3cmd](http://s3tools.org/s3cmd), including conf file

And more optional:

- [Luigi](https://github.com/spotify/luigi), including conf file for S3
- [IPython.parallel](http://ipython.org/ipython-doc/dev/parallel/) cluster creation

Using
-----

### Local VM

Just run `vagrant up`, the IPython notebook port (8888) is forwarded to the host.

### EC2

- Install vagrant aws plugin: `vagrant plugin install vagrant-aws`
- Put your AWS credentials, keypair path and security group in the `Vagrantfile`
under the `config.vm.provider :aws do |aws, override|` section
- `vagrant up --provider=aws`

### SSH

Vagrant box and EC2 instance are based on ubuntu 12.04 to be consistent even the local vagrant
image will have everything installed under the ubuntu user. Use `vagrant ssh -- -l ubuntu`
to ssh as that user.

If running on the EC2 don't need to worry about that, just `vagrant ssh`

Configuration
-------------

All settings should be located in `pillar/settings.sls`

### Python packages

Change the `salt/salt/python/requirements.txt` file


IPython.parallel cluster
------------------------

Fill the `aws` and `ipcluster` sections on `pillar/settings.sls` create the datascience box ssh into it and run:

1. `sudo salt-call state.sls ipcluster` once to start `ipcontroller` and the salt-master
2. `sudo salt-cloud -p base_ec2 ipython-minion-X`: where X is unique for every instance. This will create a new instance install the `salt-minion` and connect it to the `salt-master`
3. `sudo salt 'ipython-minion-X' saltutil.sync_all`
4. `sudo salt 'ipython-minion-X' state.sls ipcluster-minion`: will bootstrap the same python environment on the minions and start `ipenginge`

Repeat steps 2-4 for every new worker instance you need. Note that you can run step 2 a couple of times and then run steps 3 and 4 using `X=*`.

Everyting is ready, go to the notebook and do some parallel amazing work, see [IPython.parallel](http://ipython.org/ipython-doc/dev/parallel/) for more information.

**Note**: If you already have an instance running you can fill the values locally and run `vagrant provision` or just fill the values in the instance under `/srv/pillar/settings.sls`
