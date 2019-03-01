# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles


security = ModuleSecurityInfo('cpskin.workflow')

security.declarePublic('ViewPrivateContent')
ViewPrivateContent = 'View private content'
setDefaultRoles(ViewPrivateContent, (
    'Manager',
    'Site Administrator',
    'Owner',
    'Reviewer',
    'Editor',
),)
