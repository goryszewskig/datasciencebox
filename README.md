DataScienceBox
==============

My personal data science box based on [salt](http://www.saltstack.com/) and [Vagrant](http://vagrantup.com/)
to easily create cloud instances or local VMs.

Includes
--------

- Ubuntu 12.04 with `build-essential`
- Python 2.7.4 environment based on [Anaconda](http://continuum.io/downloads) 1.9
- [IPython notebook](http://ipython.org/notebook.html) running in port 8888
- [Luigi](https://github.com/spotify/luigi), including conf file for S3
- [s3cmd](http://s3tools.org/s3cmd), including conf file

Configuration
-------------

To set the salt pillar variables only need to change the `Vagrantfile` under:

```
    salt.pillar({
      "aws" => {
        "access_key" => "",
        "secret_key" => ""
      }
    })
```

To add more python packages to be installed change the `salt/roots/salt/python/requirements.txt` file

Using
-----

Local VM: `vagrant up`

EC2:
- Install vagrant aws plugin: `vagrant plugin install vagrant-aws`
- Put your AWS credentials, keypair path and security group in the `Vagrantfile`
under the `config.vm.provider :aws do |aws, override|` section
- `vagrant up --provider=aws`

### SSH

Vagrant box and EC2 instance are based on ubuntu 12.04 to be consistent even the local vagrant
image will have everything installed under the ubuntu user. Use `vagrant ssh -- -l ubuntu`
to ssh as that user.

If running on the EC2 don't need to worry about that, just `vagrant ssh`
