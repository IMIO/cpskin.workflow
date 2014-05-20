import logging

from plone.app.workflow.remap import remap_workflow

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('cpskin.workflow')


def installWorkflows(context):
    if context.readDataFile('cpskin.workflow-default.txt') is None:
        return

    logger.info('Installing workflows')
    portal = context.getSite()

    # we change the default workflow
    logger.info("Adapting default workflow and existing objects")
    wft = getToolByName(portal, 'portal_workflow')
    tt = getToolByName(portal, 'portal_types')
    # list types with a non default workflow
    nondefault = [info[0] for info in wft.listChainOverrides()]
    # list types with the default workflow
    type_ids = [type for type in tt.listContentTypes() if type not in nondefault]
    chain = '(Default)'
    if wft.getDefaultChain() == ('simple_publication_workflow',):
        wft.setDefaultChain('cpskin_workflow')
        state_map = {'private': 'created',
                     'pending': 'published_and_hidden',
                     'published': 'published_and_hidden'}
        remap_workflow(portal, type_ids=type_ids, chain=chain, state_map=state_map)
    elif wft.getDefaultChain() == ('plone_workflow',):
        wft.setDefaultChain('cpskin_workflow')
        state_map = {'private': 'created',
                     'pending': 'published_and_hidden',
                     'published': 'published_and_hidden',
                     'visible': 'published_and_hidden'}
        remap_workflow(portal, type_ids=type_ids, chain=chain, state_map=state_map)


def configureMembers(context):
    if context.readDataFile('cpskin.workflow-membersconfig.txt') is None:
        return

    logger.info('Configuring members')
    portal = context.getSite()
    wft = getToolByName(portal, 'portal_workflow')

    # Publish Members
    members = portal['Members']
    wft = portal.portal_workflow
    if wft.getInfoFor(members, 'review_state') == 'private':
        wft.doActionFor(members, 'publish_and_hide')

    # Publish help page
    if members.hasObject('help-page'):
        helpPage = members['help-page']
        wft.doActionFor(helpPage, 'publish_and_hide')


def uninstallWorkflows(context):
    if context.readDataFile('cpskin.workflow-uninstall.txt') is None:
        return

    logger.info('Uninstalling workflows')
    portal = context.getSite()

    # we change the default workflow
    logger.info("Adapting default workflow and existing objects")
    wft = getToolByName(portal, 'portal_workflow')
    tt = getToolByName(portal, 'portal_types')
    # list types with a non default workflow
    nondefault = [info[0] for info in wft.listChainOverrides()]
    # list types with the default workflow
    type_ids = [type for type in tt.listContentTypes() if type not in nondefault]
    if wft.getDefaultChain() and wft.getDefaultChain()[0].startswith('cpskin'):
        state_map = {'created': 'private',
                     'pending': 'pending',
                     'published_and_hidden': 'published',
                     'published_and_shown': 'published'}
        remap_workflow(portal, type_ids=type_ids, chain=('simple_publication_workflow',), state_map=state_map)
        wft.setDefaultChain('simple_publication_workflow')
