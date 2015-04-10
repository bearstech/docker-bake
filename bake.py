#!/usr/bin/env python

import re
import os.path
from subprocess import Popen


SPACE = re.compile("\s+")

DOCKERFILE = """
FROM debian:stable

RUN apt-get update && apt-get install -y python-pip python-dev {packages}
RUN pip install --upgrade pip wheel setuptools

ENV PYTHONUSERBASE /data/usr
ENV XDG_CACHE_HOME /cache/pip

WORKDIR /data
"""

with open('requierements.txt', 'r') as f:
    for line in f:
        if len(line) and line[0] == '#':
            tokens = SPACE.split(line[1:].strip())
            if len(tokens) > 1 and tokens[:2] == ['apt-get', 'install']:
                if not os.path.exists('/tmp/bake'):
                    os.mkdir('/tmp/bake')
                with open('/tmp/bake/Dockerfile', 'w') as d:
                    d.write(DOCKERFILE.format(packages=" ".join(tokens[2:])))
                p = Popen(['docker', 'build', '-t', 'bake', '/tmp/bake'])
                print p.wait()
                cache = os.path.expanduser('~/.bake/')
                if not os.path.exists('usr'):
                    os.mkdir('usr')
                if not os.path.exists(cache):
                    os.mkdir(cache)
                p = Popen(['docker', 'run', '--rm', '-v',
                           '%s:/data' % os.getcwd(), '-v', '%s:/cache' % cache ,
                           'bake', 'pip', 'wheel',
                           '--wheel-dir', '/cache/wheel',
                           '--use-wheel', '--find-links', '/cache/wheel',
                           '-r', 'requierements.txt'])
                print p.wait()
                p = Popen(['docker', 'run', '--rm', '-v',
                           '%s:/data' % os.getcwd(), '-v', '%s:/cache' % cache ,
                           'bake', 'pip', 'install', '--no-index', '--upgrade',
                           '--find-links', '/cache/wheel',
                           '--user', '-r', 'requierements.txt'])
                print p.wait()
