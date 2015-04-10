Bake your pip with Docker
=========================

You need Python and Docker (even Boot2docker).

Go in a folder with a requirements.txt, something like that:

    # Hop
    #
    # apt-get install     libyaml-dev    libxslt1-dev libxml2-dev
    pyYAML
    celery
    lxml

Bake it:

    ./bake.py

Enjoy your `usr` folder:

    tree usr

And enjoy your cache:

    ls ~/.bake/wheel

Licence
-------

GPL v3 ©2015 Mathieu Lecarme
