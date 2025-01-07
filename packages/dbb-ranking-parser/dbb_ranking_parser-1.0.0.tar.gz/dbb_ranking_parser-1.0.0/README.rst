==================
DBB Ranking Parser
==================

Extract league rankings from the DBB_ (Deutscher Basketball Bund e.V.)
website.

This library has been extracted from the web application behind the
website of the `BTB Royals Oldenburg`_ (a basketball team from
Oldenburg, Germany) where it has proven itself for many, many years.


Website
=======

The official micro website is at: https://homework.nwsnet.de/releases/4a51/#dbb-ranking-parser


Code Status
===========

|badge_github-actions_test|

.. |badge_github-actions_test| image:: https://github.com/homeworkprod/dbb-ranking-parser/actions/workflows/test.yml/badge.svg
   :alt: Testing Status
   :target: https://github.com/homeworkprod/dbb-ranking-parser/actions/workflows/test.yml


Requirements
============

- Python_ 3.9+
- lxml_


Installation
============

Install this package via pip_:

.. code:: sh

    $ pip install dbb-ranking-parser

Pre-built binaries (so-called Python "wheels") should be available for
supported Python versions and most architectures.

If not, however, it can be necessary to install a compiler and certain
header files (for the targeted Python_ version as well as those for
libxml2_ and libxslt_) so that lxml can be built from source.

On `Debian Linux`_, one should be able to install these from the
distribution's repositories (as the 'root' user):

.. code:: sh

    # aptitude update
    # aptitude install build-essential python3.9-dev libxml2-dev libxslt1-dev


Usage
=====

To fetch and parse a league ranking, the appropriate URL is required.

It can be obtained on the DBB_ website. On every league's ranking page
there should be a link to a (non-"XL") HTML print version.

Its target URL should look like this (assuming the league's ID is
12345):
``https://www.basketball-bund.net/public/tabelle.jsp?print=1&viewDescKey=sport.dbb.views.TabellePublicView/index.jsp_&liga_id=12345``

The league ID has to be identified manually in any of the URLs specific
for that league (ranking, schedule, stats).

For convenience, specifying only the league ID is sufficient; the URL
will be assembled automatically. (Obviously, this might break when the
URL structure changes on the DBB website.)


Programmatically
----------------

.. code:: python

    from dbbrankingparser import load_ranking_for_league


    league_id = 12345

    ranking = list(load_ranking_for_league(league_id))

    top_team = ranking[0]
    print('Top team:', top_team['name'])

The URL can be specified explicitly, too:

.. code:: python

    from dbbrankingparser import load_ranking_from_url


    URL = '<see example above>'

    ranking = list(load_ranking_from_url(URL))

Note that a call to a ``load_ranking_*`` method returns a generator. To
keep its elements around, and also to access them by index, they can be
fed into a list (as shown above).


On the Command Line
-------------------

The package includes a command line script to retrieve a league's
rankings non-programmatically, as JSON. It requires a league ID as its
sole argument:

.. code:: sh

    $ dbb-ranking-parser get 12345
    [{"name": "Team ACME", "rank": 1, …}]


Via HTTP
--------

Also included is an HTTP wrapper around the parser.

To spin up the server:

.. code:: sh

    $ dbb-ranking-parser serve
    Listening for HTTP requests on 127.0.0.1:8080 ...

The server will attempt to look up a ranking for requests with an URL
part of the form ``/<league id>``:

.. code:: sh

    $ curl http://localhost:8080/12345
    [{"name": "Team ACME", "rank": 1, …}]


Docker
======

DBB Ranking Parser can also be run in a Docker_ container. This avoids
the local creation of a virtual environment and the installation of the
packages, or be useful in a deployment where containers are used.

Building a Docker_ image requires:

- Docker_ being installed
- a source copy of the `dbb-ranking-parser` package

In the package path:

.. code:: sh

    $ docker build -t dbb-ranking-parser .

This should build a Docker_ image based upon `Alpine Linux`_ and which
includes Python_ 3, lxml_ and the DBB Ranking Parser itself. It should
be roughly 70 MB in size.

Running the Docker container accepts the same arguments as the command
line script.

To fetch a single ranking:

.. code:: sh

    $ docker run --rm dbb-ranking-parser get 12345
    [{"name": "Team ACME", "rank": 1, …}]

To spin up the HTTP server on port 7000 of the host machine:

.. code:: sh

    $ docker run -p 7000:8080 --rm dbb-ranking-parser serve --host 0.0.0.0 --port 8080

The ``--rm`` option causes a container (but not the image) to be removed
after it exits.


.. _DBB:                  https://www.basketball-bund.net/
.. _BTB Royals Oldenburg: https://www.btbroyals.de/
.. _Python:               https://www.python.org/
.. _pip:                  https://www.pip-installer.org/
.. _lxml:                 https://lxml.de/
.. _libxml2:              https://xmlsoft.org/XSLT/
.. _libxslt:              https://xmlsoft.org/XSLT/
.. _Debian Linux:         https://www.debian.org/
.. _Docker:               https://www.docker.com/
.. _Alpine Linux:         https://alpinelinux.org/


Author
======

DBB Ranking Parser was created and is maintained by Jochen Kupperschmidt.


License
=======

Copyright (c) 2006-2025 `Jochen Kupperschmidt
<http://homework.nwsnet.de/>`_

DBB Ranking Parser is licensed under the `MIT License
<https://choosealicense.com/licenses/mit/>`_.

The license text is provided in the `LICENSE <LICENSE>`_ file.
