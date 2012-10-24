.. PyManetSim documentation master file, created by sphinx-quickstart on Wed Aug 26 18:11:42 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyManetSim's documentation!
======================================
PyManetSim is a simulator for quickly test protocols in manet and ad-hoc networks. It aims at simplicity and being able to be extended to each individual need.

You should use PyManetSim if you work in want to see if an idea works. The simulator engine is simply a broker for messages and a plane in which nodes are located. The logic is that you quickly implement your test protocol and the simulator makes the boring job of simulating that messages are sent between nodes in the plane. It also deals with the passing of time.

Releases
========

The current release number is 0.1 and is a very alpha release. Future development will probably break the current API and so test PyManetSim at your own risk.

Contents
========

.. toctree::
   :maxdepth: 2

   about
   installation
   architecture_overview
   tutorials
   api
   contribute
   license

   TODO

The complete documentation is also available in PDF format at:
http://maneljakim.todo

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
