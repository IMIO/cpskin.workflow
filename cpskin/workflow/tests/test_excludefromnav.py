import unittest
from cpskin.workflow.testing import CPSKIN_WORKFLOW_INTEGRATION_TESTING
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestExcludeFromNav(unittest.TestCase):

    layer = CPSKIN_WORKFLOW_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_publish_and_hide(self):
        doc = api.content.create(
            container=self.portal, type='Document', id='doc')
        api.content.transition(obj=doc, transition='publish_and_hide')
        self.assertTrue(doc.exclude_from_nav)

    def test_publish_and_show(self):
        doc = api.content.create(
            container=self.portal, type='Document', id='doc')
        api.content.transition(obj=doc, transition='publish_and_show')
        self.assertFalse(doc.exclude_from_nav)

    def test_set_excludefromnav_change_state(self):
        folder = api.content.create(
            container=self.portal, type='Folder', id='doc')
        api.content.transition(obj=folder, transition='publish_and_show')
        self.assertFalse(folder.exclude_from_nav)
        state = api.content.get_state(obj=folder)
        self.assertEquals(state, 'published_and_shown')
        folder.exclude_from_nav = True
        notify(ObjectModifiedEvent(folder))
        state = api.content.get_state(obj=folder)
        self.assertEquals(state, 'published_and_hidden')
        folder.exclude_from_nav = False
        notify(ObjectModifiedEvent(folder))
        state = api.content.get_state(obj=folder)
        self.assertEquals(state, 'published_and_shown')
