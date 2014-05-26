import transaction
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from Products.CMFCore.utils import getToolByName

import cpskin.workflow


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


CPSKIN_WORKFLOW_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_WORKFLOW_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.workflow,
    gs_profile_id="cpskin.workflow:testing")

CPSKIN_WORKFLOW_FUNCTIONAL_TESTING = WorkflowFunctional(
    bases=(CPSKIN_WORKFLOW_FIXTURE, ),
    name="CPSkinWorkflow:Functional")

CPSKIN_WORKFLOW_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_WORKFLOW_FIXTURE,),
    name="CPSkinWorkflow:Integration")
