# exhibitor2dns

Usage:

```sh
exhibitor2dns --zone=yourzone.example.com \
              --exhibitor_url=http://your-exhibitor-endpoint.example.com/ \
              --rr=zookeeper
```

exhibitor2dns uses Boto to interact with Route53, so you have various options for providing aws credentials.  You can set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` envivonment variables, or if exhibitor2dns is running on an ec2 instance it will try to use the instance's IAM role if there is one available.  See the [Boto documentation](http://boto.readthedocs.org/en/latest/boto_config_tut.html) for more details.
