import logging

from plone.app.collection.collection import Collection
from plone.app.workflow.remap import remap_workflow

from Products.CMFCore.utils import getToolByName

from cpskin.core.utils import convertCollection
from cpskin.core.utils import reactivateTopic

logger = logging.getLogger('cpskin.workflow')


def installWorkflows(context):
    if context.readDataFile('cpskin.workflow-default.txt') is None:
        return

    logger.info('Installing workflows')
    portal = context.getSite()

    reactivateTopic()

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

    # define some navtree properties
    # we want to enable wf filtering and show only elements that are published_and_show
    logger.info("Adapting navigation")
    navtree_properties = portal.portal_properties.navtree_properties
    if navtree_properties.enable_wf_state_filtering is False:
        navtree_properties.manage_changeProperties(enable_wf_state_filtering=True,
                                                   wf_states_to_show=('published_and_shown',))


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
    chain = '(Default)'
    if wft.getDefaultChain() and wft.getDefaultChain()[0].startswith('cpskin'):
        wft.setDefaultChain('simple_publication_workflow')
        state_map = {'created': 'private',
                     'pending': 'pending',
                     'published_and_hidden': 'published',
                     'published_and_shown': 'published'}
        remap_workflow(portal, type_ids=type_ids, chain=chain, state_map=state_map)

    # we must re-create criterium on review_state who use selection_list
    # (published_and_hidden and published_and_shown) by single published value
    # for news
    if hasattr(portal, 'news') and hasattr(portal.news, 'aggregator'):
        changeStateCriteria(portal.news.aggregator, 'uninstall')
    # for event
    if hasattr(portal, 'events') and hasattr(portal.events, 'aggregator'):
        changeStateCriteria(portal.events.aggregator, 'uninstall')


def changeStateCriteria(aggregator, step):
    if isinstance(aggregator, Collection):
        aggregator = convertCollection(aggregator)
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
