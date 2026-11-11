"""Exercise the environment switch through Zope's actual ZCML loader."""

import os
import sys
import types
import unittest
from unittest.mock import patch

import zope.component
from zope.component import getGlobalSiteManager
from zope.component.testing import setUp
from zope.component.testing import tearDown
from zope.configuration import xmlconfig
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


class IWorkflowActionAdapter(Interface):
    """Stand-in for SENAITE's workflow adapter interface."""


@implementer(IWorkflowActionAdapter)
class OriginalPublishAdapter(object):
    def __init__(self, context, request):
        pass


@implementer(IWorkflowActionAdapter)
class GenericPublishAdapter(OriginalPublishAdapter):
    pass


@implementer(IBrowserRequest)
class Request(object):
    pass


ZCML = """
<configure xmlns="http://namespaces.zope.org/zope">
  <include file="{original}" />
  <include package="senaite.skippdf" />
  <includeOverrides package="senaite.skippdf" file="overrides.zcml" />
</configure>
"""


class EnvironmentZCMLTests(unittest.TestCase):
    def setUp(self):
        setUp()
        self.addCleanup(tearDown)

        # Only SENAITE's interface and factories are stand-ins. Configuration,
        # conflict resolution, and component registration use the real Zope code.
        modules = {}
        for name in ("bika", "bika.lims", "bika.lims.browser",
                     "bika.lims.browser.workflow", "bika.lims.interfaces"):
            module = types.ModuleType(name)
            module.__path__ = []
            modules[name] = module
        for name, module in modules.items():
            if "." in name:
                parent, child = name.rsplit(".", 1)
                setattr(modules[parent], child, module)
        interfaces = modules["bika.lims.interfaces"]
        interfaces.IWorkflowActionAdapter = IWorkflowActionAdapter
        workflow = modules["bika.lims.browser.workflow"]
        workflow.OriginalPublishAdapter = OriginalPublishAdapter
        workflow.WorkflowActionGenericAdapter = GenericPublishAdapter
        self.modules = patch.dict(sys.modules, modules)
        self.modules.start()
        self.addCleanup(self.modules.stop)

    def load_adapter(self, value):
        with patch.dict(os.environ):
            os.environ.pop("SENAITE_SKIP_PDF", None)
            if value is not None:
                os.environ["SENAITE_SKIP_PDF"] = value
            context = xmlconfig.file("meta.zcml", zope.component, execute=False)
            original = os.path.join(os.path.dirname(__file__), "original.zcml")
            xmlconfig.string(ZCML.format(original=original), context=context)
        return getGlobalSiteManager().queryMultiAdapter(
            (object(), Request()), IWorkflowActionAdapter,
            name="workflow_action_publish")

    def test_true_replaces_original_adapter(self):
        self.assertIs(type(self.load_adapter("true")), GenericPublishAdapter)

    def test_missing_value_preserves_original_adapter(self):
        self.assertIs(type(self.load_adapter(None)), OriginalPublishAdapter)

    def test_environment_is_read_for_each_configuration(self):
        self.assertIs(type(self.load_adapter("true")), GenericPublishAdapter)
        self.assertIs(type(self.load_adapter("false")), OriginalPublishAdapter)

    def test_other_values_preserve_original_adapter(self):
        values = ("", "false", "FALSE", "TRUE", "True", "1", "yes", " true ")
        for value in values:
            with self.subTest(value=value):
                adapter = self.load_adapter(value)
                self.assertIs(type(adapter), OriginalPublishAdapter)


if __name__ == "__main__":
    unittest.main()
