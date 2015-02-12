#!/usr/bin/env python
"""exhibitor2dns: Dynamic DNS for Exhibitor-run Zookeeper ensembles."""

import boto
import gflags
import logging
import pprint
import requests
import sys
import urlparse

gflags.DEFINE_string('zone', None, 'DNS zone name (e.g. prod.example.com)')
gflags.DEFINE_string('rr', 'zookeeper', 'Name of A record to manage')
gflags.DEFINE_string('exhibitor_url', None,
                     'Base URL to exhibitor http endpoint '
                     '(e.g. http://exhibitor.prod.example.com/)')
gflags.DEFINE_integer('ttl', 300, 'Default record TTL')

gflags.DEFINE_integer('verbosity', 20, 'Log level')
FLAGS = gflags.FLAGS


def get_zk_servers(exhibitor_url):
    url = urlparse.urljoin(exhibitor_url, '/exhibitor/v1/cluster/list')
    return requests.get(url).json()['servers']


def main():
    """main"""
    FLAGS(sys.argv)
    logging.basicConfig(level=FLAGS.verbosity)
    r53 = boto.connect_route53()
    zone = r53.get_zone(FLAGS.zone)

    target_fqdn = '%s.%s' % (FLAGS.rr, FLAGS.zone)

    exhibitor_list = get_zk_servers(FLAGS.exhibitor_url)
    logging.info('Exhibitor cluster:\n%s',
                 pprint.pformat(exhibitor_list))

    existing_record = zone.get_a(target_fqdn)

    if existing_record:
        logging.info('Existing record:\n%s',
                     pprint.pformat(existing_record.resource_records))
        if sorted(exhibitor_list) != sorted(existing_record.resource_records):
            logging.info('Updating record to match')
            zone.update_record(existing_record, exhibitor_list)
        else:
            logging.info('Up to date.')
    else:
        logging.info('Creating new record.')
        zone.add_a(target_fqdn, exhibitor_list, ttl=FLAGS.ttl)
    logging.info('Done!')


if __name__ == '__main__':
    main()
