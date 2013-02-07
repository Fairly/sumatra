"""
Utility functions for use in publishing modules


"""

import os
import errno
from urllib import urlretrieve
from urlparse import urlparse
from sumatra.projects import load_project
from sumatra.recordstore import get_record_store
from sumatra.datastore import DataKey


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def determine_project(sumatra_options):
    if 'project_dir' in sumatra_options:
        prj = load_project(sumatra_options['project_dir'])
    elif os.path.exists(os.path.join('.smt', 'project')):
        prj = load_project()
    else:
        prj = None
    return prj


def determine_record_store(prj, sumatra_options, err=Exception):
    if 'record_store' in sumatra_options:
        record_store = get_record_store(sumatra_options["record_store"])
    elif prj is None:
        raise err(
            'Neither project_dir nor record_store defined'
        )
    else:
        record_store = prj.record_store
    return record_store


def determine_project_name(prj, sumatra_options, err=Exception):
    # determine the project (short) name
    if 'project' in sumatra_options:
        project_name = sumatra_options['project']
    elif prj is None:
        raise err('project name not defined')
    else:
        project_name = prj.name
    return project_name


def get_image(record, sumatra_options, err=Exception):
    image_key = record.output_data[0]
    assert isinstance(image_key, DataKey)
    # check expected digest, if supplied, against key.digest
    if ('digest' in sumatra_options
        and sumatra_options['digest'] != image_key.digest):
        raise err('Digests do not match')
    return record.datastore.get_data_item(image_key)  # checks key.digest against file contents


def record_link_url(server_url, project_name, record_label):
    return "%s%s/%s/" % (server_url, project_name, record_label)