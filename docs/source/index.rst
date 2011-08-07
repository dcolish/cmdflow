.. CmdFlow documentation master file, created by
   sphinx-quickstart on Sun Jun 26 09:11:09 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CmdFlow's documentation!
===================================

A simple wrapper for creating shell pipelines inside python scripts

Theoretically, this can be used across platforms, but there are a few
conventions which do not translate well to Windows; i.e. `sudo` is difficult in
a system that does not use multiple simultaneous users.

.. automodule:: cmdflow

.. autoclass:: Path
   :members:

   .. automethod:: __init__

.. autoclass:: ShellOutput
   :members:

.. autoclass:: ShellCmd
   :members:

   .. automethod:: __init__


.. toctree::



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

