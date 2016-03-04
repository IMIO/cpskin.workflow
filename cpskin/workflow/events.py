from cpskin.workflow.interfaces import ICPSkinWorkflowLayer
from cpskin.workflow.interfaces import ICPSkinWorkflowWithMembersLayer
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFPlone.utils import base_hasattr


def user_initial_logged_in(event):
    """
    When a user is logged in for the first time : apply local workflow policy
    Applies only if members-config profile has been installed
    """
    portal = api.portal.get()

    request = getattr(portal, "REQUEST", None)
    if not ICPSkinWorkflowWithMembersLayer.providedBy(request):
        return

    pm = getToolByName(portal, 'portal_membership')

    # needed because happens after notifying the event we are subscribed to :
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


def object_modified_at(obj, event):
    """
    When a content is changed : check the coherence between WF state and
    'exclude from nav' parameter
    Applies only if default profile has been installed
    """
    request = getattr(obj, "REQUEST", None)
    if not ICPSkinWorkflowLayer.providedBy(request):
        return
    pw = getToolByName(obj, 'portal_workflow')
    if pw.getWorkflowsFor(obj):
        state = api.content.get_state(obj=obj)
        excludeFromNav = obj.getExcludeFromNav()

        if state == 'published_and_hidden' and not excludeFromNav:
            api.content.transition(obj=obj, transition='publish_and_show')
        elif state == 'published_and_shown' and excludeFromNav:
            api.content.transition(obj=obj, transition='publish_and_hide')


def state_modified_at(obj, event):
    """
    When a content is published (shown or hidden from nav) :
    check the coherence between WF state and 'exclude from nav' parameter
    Applies only if default profile has been installed
    """
    request = getattr(obj, "REQUEST", None)
    if not ICPSkinWorkflowLayer.providedBy(request):
        return

    state = event.new_state.id
    excludeFromNav = obj.getExcludeFromNav()
    if state == 'published_and_hidden' and not excludeFromNav:
        obj.setExcludeFromNav(True)
    elif state == 'published_and_shown' and excludeFromNav:
        obj.setExcludeFromNav(False)


# Dexterity
def object_modified(obj, event):
    """
    When a content is changed : check the coherence between WF state and
    'exclude from nav' parameter
    Applies only if default profile has been installed
    """
    request = getattr(obj, "REQUEST", None)
    if not ICPSkinWorkflowLayer.providedBy(request):
        return
    pw = getToolByName(obj, 'portal_workflow')
    if pw.getWorkflowsFor(obj):
        state = api.content.get_state(obj=obj)
        exclude_from_nav = getattr(obj, 'exclude_from_nav', None)
        if exclude_from_nav is None:
            return

        if state == 'published_and_hidden' and not exclude_from_nav:
            api.content.transition(obj=obj, transition='publish_and_show')
        elif state == 'published_and_shown' and exclude_from_nav:
            api.content.transition(obj=obj, transition='publish_and_hide')


def state_modified(obj, event):
    """
    When a content is published (shown or hidden from nav) :
    check the coherence between WF state and 'exclude from nav' parameter
    Applies only if default profile has been installed
    """
    request = getattr(obj, "REQUEST", None)
    if not ICPSkinWorkflowLayer.providedBy(request):
        return
    state = event.new_state.id
    exclude_from_nav = getattr(obj, 'exclude_from_nav', None)
    if exclude_from_nav is None:
        return
    

    if state == 'published_and_hidden' and not exclude_from_nav:
        obj.exclude_from_nav = True
    elif state == 'published_and_shown' and exclude_from_nav:
        obj.exclude_from_nav = False
