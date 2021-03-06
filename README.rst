|build-status| |coverage| |docs| |commits-since|

The refcycle package provides support for creating, analysing, and visualising
graphs of Python objects and the references between them.  It's intended to aid
in debugging reference-related problems, for example:

- Figuring out why an object is still alive after it should have been deleted.
- Detecting reference cycles that may be preventing objects from being
  collected by the regular reference-count-based garbage collection.
- Finding out why garbage collection is putting objects into ``gc.garbage``.

Features
--------

- An `ObjectGraph`_ class representing a collection of objects and references.
- Computation of `strongly connected components`_ of the object graph.
- Ability to export to JSON and reimport later for offline analysis.
- Export of images via `Graphviz`_.
- Supports Python 2 and Python 3 (CPython only).


Prerequisites
-------------

- Currently requires Python version 2.7 or version >= 3.3.  If there's any
  interest in Python 2.6 or Python 3.2 support let me know, and I may work on
  those.  It's unlikely that versions earlier than 2.6 or 3.2 will ever be
  supported.

- The `export_image`_ method for exporting a graph in image form requires
  `Graphviz`_ to be installed.

- Uses the `six`_ package to support Python 2 and Python 3 from a single
  codebase.

- Refcycle is CPython only.


Documentation
-------------

Up-to-date documentation can be found on "Read the Docs", at
http://refcycle.readthedocs.org/en/latest/index.html.


Installing refcycle
-------------------

The latest release of refcycle is available from the Python Package Index, at
https://pypi.python.org/pypi/refcycle.  On most systems, it can be installed in
the usual way using ``easy_install`` or ``pip``::

    pip install -U refcycle

The currently-in-development version can be obtained from the project's GitHub
homepage: https://github.com/mdickinson/refcycle.


License
-------

The refcycle package is copyright (c) 2013-2017 Mark Dickinson.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.


.. _Graphviz: http://www.graphviz.org
.. _six: http://pypi.python.org/pypi/six
.. _ObjectGraph: http://refcycle.readthedocs.org/en/latest/reference/object_graph.html#refcycle.object_graph.ObjectGraph
.. _export_image: http://refcycle.readthedocs.org/en/latest/reference/object_graph.html#refcycle.object_graph.ObjectGraph.export_image
.. _strongly connected components: http://en.wikipedia.org/wiki/Strongly_connected_component

.. |build-status| image:: https://travis-ci.org/mdickinson/refcycle.svg?branch=master
   :target: https://travis-ci.org/mdickinson/refcycle
   :alt: Travis CI status
.. |coverage| image:: http://codecov.io/github/mdickinson/refcycle/coverage.svg?branch=master
   :target: http://codecov.io/github/mdickinson/refcycle
   :alt: Coverage statistics from codecov.io
.. |docs| image:: https://readthedocs.org/projects/refcycle/badge/?version=latest
   :target: http://refcycle.readthedocs.org/en/latest
   :alt: Documentation build status
.. |commits-since| image:: https://img.shields.io/github/commits-since/mdickinson/refcycle/v0.2.1.svg
   :target: https://github.com/mdickinson/refcycle
   :alt: GitHub status
