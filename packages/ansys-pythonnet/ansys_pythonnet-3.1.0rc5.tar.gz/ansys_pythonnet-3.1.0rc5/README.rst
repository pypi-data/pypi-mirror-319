Ansys fork of `pythonnet <https://github.com/pythonnet/pythonnet>`_.

We will try to keep this up-to-date with pythonnet and upstream changes that might benefit the pythonnet community

Changes relative to pythonnet:

* Revert of `#1240 <https://github.com/pythonnet/pythonnet/pull/1240>`_.
* Enum REPR `#2239 <https://github.com/pythonnet/pythonnet/pull/2239>`_ is included in this release of version 3.0.2, but is unreleased in pythonnet
* Opt-into explicit interface wrapping, `#19 <https://github.com/ansys/ansys-pythonnet/pull/19>`_. This opts into the behavior that became the default in #1240 if ToPythonAs<T> is explicitly used
