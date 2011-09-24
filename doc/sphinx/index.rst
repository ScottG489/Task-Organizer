.. Task-Organizer documentation master file, created by
   sphinx-quickstart on Mon Sep 19 00:54:18 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |task-package| replace:: :ref:`task package<task-package>`
.. |task.Task| replace:: :class:`task.Task`
.. |task.TaskCreator| replace:: :class:`task.TaskCreator`
.. |task.TaskCreator.build| replace:: :func:`task.TaskCreator.build`
.. |controller.Controller| replace:: :class:`controller.Controller`
.. |examples| replace::  :ref:`examples<examples>`

Welcome to Task-Organizer's documentation!
==========================================
This documentation overviews the Task-Organizer project. This includes the
|task-package|, an :ref:`implementation <examples>`,
and it's :ref:`unit tests <unit-tests>`.

.. toctree::
   :maxdepth: 2

Basic usage
===========
A typical use case of the |task-package| will consists of creating a
|task.Task| instance via |task.TaskCreator.build| and a |controller.Controller|
instance specifying at least a *storage_type*. The |task.Task| instance can 
then be passed to any function of the |controller.Controller| instance and it
will access |task.Task|'s stored in the storage medium previously specified as
*storage_type*.

Here is a short example::

    import task
    import controller

    my_dict = {'title':'task title', 'notes':'task notes'}

    task_controller = controller.Controller('sqlite')
    task_item = task.TaskCreator.build(my_dict)

    task_controller.add(task_item)

    print task_controller.find(task_item)

This would output something like::

    ID: 1
    Title: task title
    Notes: task notes

.. note:: When importing the task and controller modules, be sure they are in your $PYTONPATH

See the |examples| section below for a full command line interface client
implementation using the |task-package|. To view the source code click on
the ``[source]`` link.

.. _task-package:

1. task Package
===============
1.1. task.controller Module
---------------------------
.. automodule:: controller
    :members:

1.2. task.storage Module
------------------------
.. automodule:: storage
    :members:

1.3. task.task Module
---------------------
.. automodule:: task
    :members:


.. _examples:

2. Examples
===========
2.1. cliparser Module
---------------------
.. automodule:: cliparser
    :members:

2.1. ctask Script
-----------------
.. automodule:: ctask
    :members:


.. _unit-tests:

3. Unit Tests
=============
3.1. test_cliparser Tests
-------------------------
.. automodule:: test_cliparser
    :members:

3.1. test_taskcontroller Tests
------------------------------
.. automodule:: test_taskcontroller
    :members:

3.1. test_task Tests
--------------------
.. automodule:: test_task
    :members:

3.1. test_taskstorage Tests
---------------------------
.. automodule:: test_taskstorage
    :members:

Project Notes
=============

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

