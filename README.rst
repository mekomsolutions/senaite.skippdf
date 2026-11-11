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


Enabling the override
---------------------

Set ``SENAITE_SKIP_PDF=true`` in the SENAITE process environment before
starting the instance::

    SENAITE_SKIP_PDF=true


During ZCML configuration, the add-on reads the environment and provides
the ``senaite-skip-pdf`` feature only when enabled. The adapter in
``overrides.zcml`` is guarded by ``zcml:condition="have senaite-skip-pdf"``.
