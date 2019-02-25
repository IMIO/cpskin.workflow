# -*- coding: utf-8 -*-

from plone.app.workflow.remap import remap_workflow
from zope.component import queryUtility
from zope.ramcache.interfaces.ram import IRAMCache


def add_private_view(context):
    context.runAllImportStepsFromProfile('profile-cpskin.workflow:default')


def to_one(context):
    context.runImportStepFromProfile('profile-cpskin.workflow:to1', 'workflow')
    chain = ('cpskin_collective_contact_workflow',)
    types = ('held_position',
             'organization',
             'person',
             'position')
    state_map = {'active': 'active',
                 'deactivated': 'deactivated'}
    remap_workflow(context, type_ids=types, chain=chain,
                   state_map=state_map)
    util = queryUtility(IRAMCache)
    if util is not None:
        util.invalidateAll()
