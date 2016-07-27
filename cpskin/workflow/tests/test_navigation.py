import unittest
from plone.testing.z2 import Browser

from cpskin.workflow.testing import CPSKIN_WORKFLOW_FUNCTIONAL_TESTING


class TestNavigation(unittest.TestCase):

    layer = CPSKIN_WORKFLOW_FUNCTIONAL_TESTING

    def setUp(self):
        """
        Configure browser and log in to the portal as manager
        """
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.open("%s/login_form" % self.portal_url)
        self.browser.getControl(name='__ac_name').value = 'test_manager'
        self.browser.getControl(name='__ac_password').value = 'secret'
        self.browser.getControl(name='submit').click()
        self.browser.getLink('Continue to the Plone site home page').click()

    def testObjectModification(self):
        browser = self.browser
        browser.getLink(id='document').click()
        browser.getControl('Title').value = u"Test Page"
        browser.getControl('Save').click()
        self.failUnless('Changes saved' in browser.contents)
        self.failUnless('<span class="state-created">Created</span>' in browser.contents)
        browser.getLink(id='workflow-transition-publish_and_show').click()
        self.failUnless('<span class="state-published_and_shown">Published and shown</span>' in browser.contents)
        browser.getLink(text='Edit').click()
        self.assertEquals(browser.getControl(name='excludeFromNav:boolean').value,
                          False)
        browser.getControl(name='excludeFromNav:boolean').value = True
        browser.getControl('Save').click()
        self.failUnless('<span class="state-published_and_hidden">Published and hidden</span>' in browser.contents)
        browser.getLink(text='Edit').click()
        self.assertEquals(browser.getControl(name='excludeFromNav:boolean').value,
                          True)
        browser.getControl(name='excludeFromNav:boolean').value = False
        browser.getControl('Save').click()
        self.failUnless('<span class="state-published_and_shown">Published and shown</span>' in browser.contents)

    def testWorkflowModification(self):
        browser = self.browser
        browser.getLink(id='document').click()
        browser.getControl('Title').value = u"Test Page"
        browser.getControl('Save').click()
        self.failUnless('Changes saved' in browser.contents)
        self.failUnless('<span class="state-created">Created</span>' in browser.contents)
        browser.getLink(id='workflow-transition-publish_and_show').click()
        self.failUnless('<span class="state-published_and_shown">Published and shown</span>' in browser.contents)
        browser.getLink(text='Edit').click()
        self.assertEquals(browser.getControl(name='excludeFromNav:boolean').value,
                          False)
        browser.getControl('Cancel').click()
        browser.getLink(id='workflow-transition-publish_and_hide').click()
        self.failUnless('<span class="state-published_and_hidden">Published and hidden</span>' in browser.contents)
        browser.getLink(text='Edit').click()
        self.assertEquals(browser.getControl(name='excludeFromNav:boolean').value,
                          True)
        browser.getControl('Cancel').click()
