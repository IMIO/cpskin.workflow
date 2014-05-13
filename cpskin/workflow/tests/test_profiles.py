import unittest2 as unittest

from plone.app.testing import applyProfile

from Products.CMFCore.utils import getToolByName

from cpskin.workflow.testing import CPSKIN_WORKFLOW_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_WORKFLOW_INTEGRATION_TESTING

    def test_default_profile(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('cpskin_workflow' in workflow)
        self.assertTrue('cpskin_moderation_workflow' in workflow)
        self.assertFalse('readonly_workflow' in workflow)

    def test_members_profile(self):
        portal = self.layer['portal']
        applyProfile(portal, 'cpskin.workflow:members-configuration')
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('readonly_workflow' in workflow)

    def test_uninstall_profile(self):
        portal = self.layer['portal']
        applyProfile(portal, 'cpskin.workflow:uninstall')
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertFalse('cpskin_workflow' in workflow)
        self.assertFalse('cpskin_moderation_workflow' in workflow)

    def test_complete_uninstall(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        applyProfile(portal, 'cpskin.workflow:members-configuration')
        self.assertTrue('cpskin_workflow' in workflow)
        self.assertTrue('cpskin_moderation_workflow' in workflow)
        self.assertTrue('readonly_workflow' in workflow)
        applyProfile(portal, 'cpskin.workflow:uninstall')
        self.assertFalse('cpskin_workflow' in workflow)
        self.assertFalse('cpskin_moderation_workflow' in workflow)
        self.assertFalse('readonly_workflow' in workflow)
