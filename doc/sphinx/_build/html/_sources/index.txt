.. Task-Organizer documentation master file, created by
   sphinx-quickstart on Mon Sep 19 00:54:18 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |task-package| replace:: :ref:`task package<task-package>`
.. |task.Task| replace:: :class:`task.Task`
.. |task.TaskCreator| replace:: :class:`task.TaskCreator`
.. |task.TaskCreator.build| replace:: :func:`task.TaskCreator.build`
.. |controller.Controller| replace:: :class:`controller.Controller`
.. |examples| replace:: :ref:`examples<examples>`
.. |ctask| replace:: :ref:`ctask.py<ctask>`
.. |test-package| replace:: :ref:`test package<unit-tests>`

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

.. note:: When importing the task and controller modules, be sure they are in your $PYTHONPATH

See the |examples| section below for a full command line interface client
implementation using the |task-package|. To view the source code click on
the ``[source]`` link.


.. _task-package:

1. task Package
===============
The main entry point of this package is the controller module. It's meant to
be used as the API for manipulating tasks. Within the controller module is
the Controller class. When instantiated it's given the name of the desired
storage type and other optional parameters. The StorageFactory class is called
and returns an instance of the specified storage type.

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
.. _ctask:

2.1. ctask Script
-----------------
.. automodule:: ctask
    :members:


.. _unit-tests:

3. Unit Tests
=============
3.1. test_ctask Tests
-------------------------
.. automodule:: test_ctask
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
The Task-Organizer project is broken up into three parts: the task package, it's
tests, and an example command line program to show some functionality of the
package.

The |task-package| consists of the task module, used for creating an actual task,
the storage module, used to persist tasks in various types of storage, and the
controller module, which is the API to be used by external applications.

The |ctask| script is an example program included with the project that uses
this API. It consists of the ctask script itself along with the CLIParser class
that does most of the work by parsing the command line. The ctask script uses
the structured parsed arguments from the CLIParser to call the API
accordingly. It also outputs useful information according to what the API
returns.

The |test-package| tests all all of the task package's and example code's public
members. The project used a
`test-driven development <http://en.wikipedia.org/wiki/Test-driven_development>`_
(TDD) software development process, meaning that when a new class or function
was needed, it's tests were written first. This helped with the planning of
new features since writing the tests first makes the developer think about how
the added features are going to be used when implemented. It also kept the
code very stable throughout the development process since whenever a bug
arose, the tests caught it.

Development Process
-------------------
Throughout the project's development, certain development goals were held:

* A goal of 100% code `coverage <http://netbatchelder.com/code/coverage/>`_ 
  was sought regarding tests.
* All code was to strictly adhere to `pylint <http://www.logilab.org/857>`_
  complaints.
* All tests must pass before pushing out any code to the master repository.

along with various development practices:

* All coding was done with command line tools on Arch Linux on the Bash shell.
* vim was used as the IDE to write all code. Various plugins were used to help
  with coding such as `ropevim <rope.sourceforge.net/ropevim.html>`_.
* screen was used with each source file open in vim in a separate window. This
  made it easy to reference or change any file.
* git was used for source control. `github <https://www.github.com>`_ was used
  as the master repository.
* The test.sh shell script was created to make testing as simple as possible.
* Directories were kept as clean as possible of unneeded storage, \*.pyc,
  or other extraneous files.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

