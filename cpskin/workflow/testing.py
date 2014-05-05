from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig


class CPSkinWorkflow(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import cpskin.workflow
        xmlconfig.file('configure.zcml', cpskin.workflow, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.workflow:default')


CPSKIN_WORKFLOW_FIXTURE = CPSkinWorkflow()

CPSKIN_WORKFLOW_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_WORKFLOW_FIXTURE,),
    name="CPSkinWorkflow:Integration")
