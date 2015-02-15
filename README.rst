=============
exhibitor2dns
=============

.. image:: https://travis-ci.org/benley/exhibitor2dns.svg?branch=master
    :target: https://travis-ci.org/benley/exhibitor2dns

Exhibitor2dns will keep a round-robin A record in sync with the state of a
Zookeeper ensemble managed by the excellent Exhibitor_ supervisor `from
Netflix`_.  This is particularly useful if your Zookeeper nodes are in an
autoscaling group, or any other setup where you don't have fixed IP addresses
for your Zookeeper servers.

Usage::

  exhibitor2dns --zone=yourzone.example.com \
                --exhibitor_url=http://your-exhibitor-endpoint.example.com/ \
                --rr=zookeeper

exhibitor2dns uses Boto to interact with Route53, so you have various options
for providing aws credentials.  You can set ``AWS_ACCESS_KEY_ID`` and
``AWS_SECRET_ACCESS_KEY`` envivonment variables, or if exhibitor2dns is running
on an ec2 instance it will try to use the instance's IAM role if there is one
available.  See the `Boto documentation`_ for more details.

.. _Boto Documentation: http://boto.readthedocs.org/en/latest/boto_config_tut.html
.. _Exhibitor: https://github.com/Netflix/exhibitor
.. _From Netflix: http://techblog.netflix.com/2012/04/introducing-exhibitor-supervisor-system.html
