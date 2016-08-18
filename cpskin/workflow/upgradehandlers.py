# -*- coding: utf-8 -*-

from ftw.upgrade.workflow import WorkflowChainUpdater
from ftw.upgrade import UpgradeStep


class UpdateWorkflowChains(UpgradeStep):

    def __call__(self):
        query = {'portal_type': [
            'held_position',
            'organization',
            'person',
            'position',
        ]}
        objects = self.catalog_unrestricted_search(query, full_objects=True)

        review_state_mapping = {
            ('collective_contact_workflow', 'cpskin_collective_contact_workflow'): {
                'active': 'published',
                'deactivated': 'created'}}

        with WorkflowChainUpdater(objects, review_state_mapping):
            self.setup_install_profile('profile-cpskin.workflow:to1')
