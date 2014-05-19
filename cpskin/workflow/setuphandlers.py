import logging

from plone.app.workflow.remap import remap_workflow

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('cpskin.workflow')


def installWorkflows(context):
    if context.readDataFile('cpskin.workflow-default.txt') is None:
        return

    logger.info('Installing workflows')
    portal = context.getSite()

    # we must re-create criterium on review_state who use single published
    # value by selection_list (published_and_hidden and published_and_shown)
    # for news
    if hasattr(portal, 'news') and hasattr(portal.news, 'aggregator'):
        changeStateCriteria(portal.news.aggregator, 'install')
    # for event
    if hasattr(portal, 'events') and hasattr(portal.events, 'aggregator'):
        changeStateCriteria(portal.events.aggregator, 'install')

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

    # Publish Members
    members = portal['Members']
    wft = portal.portal_workflow
    if wft.getInfoFor(members, 'review_state') == 'private':
        wft.doActionFor(members, 'publish_and_hide')


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

    # we must re-create criterium on review_state who use selection_list
    # (published_and_hidden and published_and_shown) by single published value
    # for news
    if hasattr(portal, 'news') and hasattr(portal.news, 'aggregator'):
        changeStateCriteria(portal.news.aggregator, 'uninstall')
    # for event
    if hasattr(portal, 'events') and hasattr(portal.events, 'aggregator'):
        changeStateCriteria(portal.events.aggregator, 'uninstall')


def changeStateCriteria(aggregator, step):
    criteria = aggregator.listCriteria()
    # 1 : delete old criterions and get expires, end fields
    isexpires_field = False
    isend_field = False
    for criterion in criteria:
        if (criterion.field == 'review_state') and (criterion.archetype_name != 'Sort Criterion'):
            aggregator.deleteCriterion(criterion.getId())
        if (criterion.field == 'start') and (criterion.archetype_name != 'Sort Criterion'):
            aggregator.deleteCriterion(criterion.getId())
        if criterion.field == 'end':
            isend_field = True
        if criterion.field == 'expires':
            isexpires_field = True
    # 2 : create new 'cpskin' criterion
    if step == 'install':
        criterion = aggregator.addCriterion(field='review_state', criterion_type='ATSelectionCriterion')
        criterion.setValue(('published_and_hidden', 'published_and_shown'))
    else:
        criterion = aggregator.addCriterion(field='review_state', criterion_type='ATSimpleStringCriterion')
        criterion.setValue('published')
    # 3 : adapt news and events criterion
    parentObj = aggregator.aq_inner.aq_parent
    if parentObj.id == 'events' and not isend_field:
        criterion = aggregator.addCriterion(field='end', criterion_type='ATFriendlyDateCriteria')
        criterion.setValue(None)
        criterion.setOperation('more')
        criterion.setDateRange('+')
    if parentObj.id == 'news' and not isexpires_field:
        criterion = aggregator.addCriterion(field='expires', criterion_type='ATFriendlyDateCriteria')
        criterion.setValue(None)
        criterion.setOperation('more')
        criterion.setDateRange('+')
