# -*- coding: utf-8 -*-
from plone.app.workflow.remap import remap_workflow
from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger('cpskin.workflow')


def installWorkflows(context):
    if context.readDataFile('cpskin.workflow-default.txt') is None:
        return

    logger.info('Installing workflows')
    portal = context.getSite()

    # We configure the calendar
    pc = getToolByName(portal, 'portal_calendar')
    pc.calendar_states = ('published_and_hidden', 'published_and_shown')

    # We change the default workflow
    logger.info('Adapting default workflow and existing objects')
    wft = getToolByName(portal, 'portal_workflow')
    if wft.getDefaultChain() == ('simple_publication_workflow',):
        state_map = {'private': 'created',
                     'pending': 'published_and_hidden',
                     'published': 'published_and_hidden'}
        changeDefaultWorkflowAndRemap(portal, state_map, 'cpskin_workflow')
    elif wft.getDefaultChain() == ('plone_workflow',):
        state_map = {'private': 'created',
                     'pending': 'published_and_hidden',
                     'published': 'published_and_hidden',
                     'visible': 'published_and_hidden'}
        changeDefaultWorkflowAndRemap(portal, state_map, 'cpskin_workflow')


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

    # We configure the calendar
    pc = getToolByName(portal, 'portal_calendar')
    pc.calendar_states = ('published')

    # We change the default workflow
    logger.info('Adapting default workflow and existing objects')
    wft = getToolByName(portal, 'portal_workflow')
    if wft.getDefaultChain() and wft.getDefaultChain()[0].startswith('cpskin'):
        state_map = {'created': 'private',
                     'pending': 'pending',
                     'published_and_hidden': 'published',
                     'published_and_shown': 'published'}
        changeDefaultWorkflowAndRemap(
            portal,
            state_map,
            'simple_publication_workflow')


def changeDefaultWorkflowAndRemap(portal, state_map, new_wf):
    wft = getToolByName(portal, 'portal_workflow')
    tt = getToolByName(portal, 'portal_types')
    # List types with a non default workflow
    nondefault = [info[0] for info in wft.listChainOverrides()]
    # List types with the default workflow
    type_ids = [type for type in tt.listContentTypes() if type not in nondefault]  # noqa
    wft.setChainForPortalTypes(type_ids, wft.getDefaultChain())
    wft.setDefaultChain(new_wf)
    remap_workflow(
        portal, type_ids=type_ids, chain=(new_wf,), state_map=state_map)
    wft.setChainForPortalTypes(type_ids, '(Default)')
