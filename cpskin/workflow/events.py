from plone import api

from Products.CMFPlone.utils import base_hasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id


def user_initial_logged_in(event):
    """
    When a user is logged in for the first time : apply local workflow policy
    """
    portal = api.portal.get()
    pm = getToolByName(portal, 'portal_membership')

    # XXX needed because happens after notifying the event we are subscribed to
    pm.createMemberArea()

    home = pm.getHomeFolder()
    if home is None:
        return

    # XXX see if refactoring is possible
    if not base_hasattr(home, WorkflowPolicyConfig_id):
        home.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        pc = getattr(home, WorkflowPolicyConfig_id)
        pc.setPolicyIn('members-policy')
        pc.setPolicyBelow('members-policy')
        # Update security on home
        pwf = getToolByName(portal, 'portal_workflow')
        wfs = {}
        for id in pwf.objectIds():
            wf = pwf.getWorkflowById(id)
            if base_hasattr(wf, 'updateRoleMappingsFor'):
                wfs[id] = wf
        pwf._recursiveUpdateRoleMappings(home, wfs)
        # Give local roles to owner
        home.manage_addLocalRoles(pm.getAuthenticatedMember().getId(),
                                  ['Contributor', 'Editor', 'Reader'])
        home.manage_permission('Review portal content',
                               ('Manager', 'Site Administrator', 'Reviewer'),
                               acquire=0)
