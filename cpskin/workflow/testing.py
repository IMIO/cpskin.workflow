from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from Products.CMFCore.utils import getToolByName
# from zope.configuration import xmlconfig

import cpskin.workflow
import transaction


class CPSkinWorkflowPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """

    def setUpZope(self, app, configurationContext):
        super(CPSkinWorkflowPloneWithPackageLayer,
              self).setUpZope(app, configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)
        import plone.app.event
        self.loadZCML(package=plone.app.event)
        # import plone.app.contenttypes
        # xmlconfig.file(
        #     'configure.zcml',
        #     plone.app.contenttypes,
        #     context=configurationContext
        # )

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'cpskin.workflow:testing')
        portal.portal_workflow.setDefaultChain('cpskin_workflow')

    def tearDownPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:uninstall')


def create_users(portal):
    acl_users = getToolByName(portal, 'acl_users')
    acl_users.userFolderAddUser('test_sitemanager', 'secret', ['Manager'], [])
    acl_users.userFolderAddUser('test_manager', 'secret', ['Manager'], [])
    acl_users.portal_role_manager.assignRolesToPrincipal(['Manager'],
                                                         'test_manager')


class WorkflowFunctional(FunctionalTesting):

    def testSetUp(self):
        super(WorkflowFunctional, self).testSetUp()
        create_users(self['portal'])
        transaction.commit()


CPSKIN_WORKFLOW_FIXTURE = CPSkinWorkflowPloneWithPackageLayer(
    name="CPSKIN_WORKFLOW_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.workflow,
    gs_profile_id="cpskin.workflow:testing")


CPSKIN_WORKFLOW_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_WORKFLOW_FIXTURE,),
    name="CPSkinWorkflow:Integration")


class CPSkinATWorkflowPloneWithPackageLayer(PloneWithPackageLayer):
    """ Use for testing Archetypes content types
    """

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        applyProfile(portal, 'Products.CMFPlone:plone')
        applyProfile(portal, 'Products.CMFPlone:testfixture')
        applyProfile(portal, 'Products.CMFPlone:plone-content')
        applyProfile(portal, 'cpskin.workflow:testing')
        portal.portal_workflow.setDefaultChain('cpskin_workflow')

    def tearDownPloneSite(self, portal):
        applyProfile(portal, 'cpskin.workflow:uninstall')


CPSKIN_AT_WORKFLOW_FIXTURE = CPSkinATWorkflowPloneWithPackageLayer(
    name="CPSKIN_AT_WORKFLOW_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.workflow,
    gs_profile_id="cpskin.workflow:testing")


CPSKIN_AT_WORKFLOW_FUNCTIONAL_TESTING = WorkflowFunctional(
    bases=(CPSKIN_AT_WORKFLOW_FIXTURE, ),
    name="CPSkinWorkflow:Functional")


# CPSKIN_AT_WORKFLOW_INTEGRATION_TESTING = IntegrationTesting(
#     bases=(CPSKIN_AT_WORKFLOW_FIXTURE,),
#     name="CPSkinWorkflow:Integration")
