#!/usr/bin/env python

import re
import os.path
from subprocess import Popen


SPACE = re.compile("\s+")

INSTALL = """#!/bin/bash
set -e

if [ ! -e /data/usr/bin/pip ]; then
    PIP=pip
    if [ -e /usr/bin/pip3 ]; then
        PIP=pip3;
    fi
    $PIP install --upgrade --user --download-cache=/cache/pip pip wheel setuptools;
fi

/data/usr/bin/pip wheel --wheel-dir /cache/wheel --cache-dir /cache/pip --use-wheel --find-links /cache/wheel -r requirements.txt

/data/usr/bin/pip install --no-index --upgrade --find-links /cache/wheel --user -r requirements.txt
"""

DOCKERFILE = """
FROM debian:{debian}

RUN apt-get update && apt-get install -y python-pip python-dev {packages}

ENV PYTHONUSERBASE /data/usr

COPY install /opt/install

WORKDIR /data
CMD ["/bin/bash", "/opt/install"]
"""

DOCKERFILE_3 = """
FROM debian:{debian}

RUN apt-get update && apt-get install -y python3-pip python3-dev {packages}
#RUN pip3 install --upgrade pip wheel setuptools

ENV PYTHONUSERBASE /data/usr

COPY install /opt/install

WORKDIR /data
CMD ["/bin/bash", "/opt/install"]
"""


def mkdir_p(path):
    if not os.path.exists(path):
        os.mkdir(path)

packages = []
python = '2.7'
debian = 'wheezy'

with open('requirements.txt', 'r') as f:
    for line in f:
        if len(line) and line[0] == '#':
            tokens = SPACE.split(line[1:].strip())
            if len(tokens) == 0:
                continue
            if len(tokens) > 1 and tokens[:2] == ['apt-get', 'install']:
                packages = tokens[2:]
            tokens = [a.lower() for a in tokens]
            if 'jessie' in tokens:
                debian = 'jessie'
            if '3.4' in tokens:
                python = '3.4'
            elif 'pypy' in tokens:
                python = 'pypy'

if debian == 'wheezy' and python == '3.4':
    raise Exception('Choose Jessie, please, for python 3.4')

print "Using python {python} on a {debian}\n".format(debian=debian,
                                                     python=python)

if python == '2.7':
    tpl = DOCKERFILE
elif python == '3.4':
    tpl = DOCKERFILE_3
elif python == 'pypy':
    pass  # TODO

mkdir_p('/tmp/bake')
with open('/tmp/bake/Dockerfile', 'w') as d:
    d.write(tpl.format(debian=debian, packages=" ".join(packages)))
with open('/tmp/bake/install', 'w') as d:
    d.write(INSTALL)

tag = 'bake:%s-%s' % (python, debian)
p = Popen(['docker', 'build', '-t', tag, '/tmp/bake'])
assert p.wait() == 0

cache = os.path.expanduser('~/.bake/')
mkdir_p(cache)
mkdir_p('usr')

p = Popen(['docker', 'run', '--rm', '-v', '%s:/data' % os.getcwd(),
           '-v', '%s:/cache' % cache, tag])
assert p.wait() == 0
