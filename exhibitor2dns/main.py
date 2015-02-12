#!/usr/bin/env python
"""exhibitor2dns: Dynamic DNS for Exhibitor-run Zookeeper ensembles."""

import argparse
import boto
import logging
import requests


def parse_args():
    """Parse commandline args."""
    parser = argparse.ArgumentParser(description=__doc__)
    required = parser.add_argument_group('Required flags')
    required.add_argument(
        '--zone', required=True, type=str,
        help='DNS zone name (e.g. prod.example.com)')
    required.add_argument(
        '--rr', type=str, required=True,
        help='Name of A record to manage. '
             'Concatenated with the value of --zone unless it ends in a "."')
    required.add_argument(
        '--exhibitor_url', required=True, metavar='URL', type=str,
        help='Base URL to exhibitor http endpoint '
             '(e.g. http://exhibitor.prod.example.com/)')
    parser.add_argument(
        '--ttl', default=300, type=int,
        help='Default record TTL (default: %(default)s)')
    parser.add_argument(
        '--verbosity', default=20, type=int, metavar='N',
        help='Log level (default: %(default)s)')
    return parser.parse_args()


def get_zk_servers(exhibitor_url):
    """Query Exhibitor's REST api and get the current list of servers."""
    url = '.'.join([exhibitor_url, '/exhibitor/v1/cluster/list'])
    return requests.get(url).json()['servers']


def main():
    """main"""
    args = parse_args()
    logging.basicConfig(level=args.verbosity)
    r53 = boto.connect_route53()
    zone = r53.get_zone(args.zone)

    if args.rr[-1] == '.':
        target_fqdn = args.rr
    else:
        target_fqdn = '%s.%s.' % (args.rr, args.zone)

    logging.info('Managing route53 record: %s', target_fqdn)

    exhibitor_list = get_zk_servers(args.exhibitor_url)
    logging.info('Exhibitor cluster:\n%s', exhibitor_list)

    existing_record = zone.get_a(target_fqdn)

    if existing_record:
        logging.info('Existing record:%s', existing_record.resource_records)
        if sorted(exhibitor_list) != sorted(existing_record.resource_records):
            logging.info('Updating record to match')
            zone.update_record(existing_record, exhibitor_list)
        else:
            logging.info('Up to date.')
    else:
        logging.info('Creating new record.')
        zone.add_a(target_fqdn, exhibitor_list, ttl=args.ttl)
    logging.info('Done!')


if __name__ == '__main__':
    main()
