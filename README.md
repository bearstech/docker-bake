Bake your pip with Docker
=========================

Install your beloved python packages, in a [user base directory](https://docs.python.org/2/library/site.html#site.USER_BASE), right here.

You can choose your Python version (2.7 or 3.4) and Debian version (Wheezy or Jessie).

Python and Docker (even Boot2docker) are needed.

No options, no configuration, just annotations in the `requirements.txt`.

Sources and wheels are cached.

Using it
--------

Go in a folder with a requirements.txt, something like that:

    # Hop
    # This demo uses python 3.4 on a Jessie
    #
    # apt-get install     libyaml-dev    libxslt1-dev libxml2-dev
    pyYAML
    celery
    lxml

Python and Debian versions are guessed from the comments.

Bake it:

    ./bake

Enjoy your `usr` folder:

    tree usr

And enjoy your cache:

    ls ~/.bake/*

Licence
-------

GPL v3 ©2015 Mathieu Lecarme
