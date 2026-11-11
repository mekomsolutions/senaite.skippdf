senaite.skippdf
==============

A minimal SENAITE add-on that overrides ``workflow_action_publish`` with
``bika.lims.browser.workflow.WorkflowActionGenericAdapter``. The adapter
registration is in ``src/senaite/skippdf/overrides.zcml`` and is disabled
by default.

Installation
------------

Add the package to your SENAITE buildout's eggs::

    [buildout]
    eggs +=
        senaite.skippdf

For a local checkout, also add its path to ``develop``::

    [buildout]
    develop +=
        /path/to/senaite.skippdf

Run ``bin/buildout`` and restart the instance. Plone's
``z3c.autoinclude.plugin`` entry point loads the ZCML, including
``overrides.zcml``, automatically. No GenericSetup profile or installation
through the Add-ons control panel is needed.

Enabling the override
---------------------

Set ``SENAITE_SKIP_PDF=true`` in the SENAITE process environment before
starting the instance, for example::

    SENAITE_SKIP_PDF=true bin/instance fg

Only the exact, case-sensitive value ``true`` enables the override.
Unset, empty, ``false``, and all other values leave the normal SENAITE
publish adapter in place.

During ZCML configuration, the add-on reads the environment and provides
the ``senaite-skip-pdf`` feature only when enabled. The adapter in
``overrides.zcml`` is guarded by ``zcml:condition="have senaite-skip-pdf"``.

The setting applies to all sites in the instance and is evaluated at
startup. Restart the instance after changing it; unset it or set it to
``false`` to disable the override.

License
-------

Mozilla Public License 2.0 (see ``LICENSE``).

Testing
-------

In a Python 3 virtual environment, run::

    pip install -r tests/requirements.txt
    PYTHONPATH=src python -m unittest discover -s tests -v

The tests use Zope's ZCML loader and component registry with stand-ins for
SENAITE's interface and adapter factories; a running SENAITE instance is
not required.
