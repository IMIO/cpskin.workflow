import unittest2 as unittest
from plone.app.testing import applyProfile
from Products.CMFCore.utils import getToolByName

from cpskin.workflow.testing import CPSKIN_WORKFLOW_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_WORKFLOW_INTEGRATION_TESTING

    def test_workflow_installed(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('cpskin_workflow' in workflow)
        self.assertTrue('cpskin_moderation_workflow' in workflow)

    def test_workflow_uninstalled(self):
        portal = self.layer['portal']
        applyProfile(portal, 'cpskin.workflow:uninstall')
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertFalse('cpskin_workflow' in workflow)
        self.assertFalse('cpskin_moderation_workflow' in workflow)
