import unittest

from plone.app.testing import (applyProfile, login, TEST_USER_NAME, setRoles,
                               TEST_USER_ID)

from Products.CMFCore.utils import getToolByName

from cpskin.workflow.testing import CPSKIN_AT_WORKFLOW_FUNCTIONAL_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_AT_WORKFLOW_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_default_profile(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('cpskin_workflow' in workflow)
        self.assertTrue('cpskin_moderation_workflow' in workflow)
        self.assertTrue('cpskin_collective_contact_workflow' in workflow)
        self.assertFalse('cpskin_readonly_workflow' in workflow)

    def test_uninstall_profile(self):
        portal = self.layer['portal']
        applyProfile(portal, 'cpskin.workflow:uninstall')
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertFalse('cpskin_workflow' in workflow)
        self.assertFalse('cpskin_moderation_workflow' in workflow)
        self.assertFalse('cpskin_collective_contact_workflow' in workflow)

    def test_complete_uninstall(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue('cpskin_workflow' in workflow)
        self.assertTrue('cpskin_moderation_workflow' in workflow)
        self.assertTrue('cpskin_collective_contact_workflow' in workflow)
        applyProfile(portal, 'cpskin.workflow:uninstall')
        self.assertFalse('cpskin_workflow' in workflow)
        self.assertFalse('cpskin_moderation_workflow' in workflow)
        self.assertFalse('cpskin_collective_contact_workflow' in workflow)

    def test_uninstall_workflows_with_public_object(self):
        from plone import api
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        obj = api.content.create(type='Document', title='My Content',
                                 container=self.portal)
        api.content.transition(obj=obj, transition='publish_and_hide')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'published_and_hidden')
        applyProfile(self.portal, 'cpskin.workflow:uninstall')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'published')

    def test_uninstall_workflows_with_private_object(self):
        from plone import api
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        obj = api.content.create(type='Document',
                                 title='My private Content',
                                 container=self.portal)
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'created')
        applyProfile(self.portal, 'cpskin.workflow:uninstall')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'private')

    def test_reinstall_profile(self):
        from plone import api
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        obj = api.content.create(type='Document',
                                 title='My private Content',
                                 container=self.portal)
        api.content.transition(obj=obj, transition='publish_and_hide')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'published_and_hidden')
        applyProfile(self.portal, 'cpskin.workflow:uninstall')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'published')
        applyProfile(self.portal, 'cpskin.workflow:default')
        state = api.content.get_state(obj=obj)
        self.assertEqual(state, 'published_and_hidden')
