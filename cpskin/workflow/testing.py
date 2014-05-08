from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting

import cpskin.workflow


CPSKIN_WORKFLOW_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_WORKFLOW_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.workflow,
    gs_profile_id="cpskin.workflow:testing")

CPSKIN_WORKFLOW_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_WORKFLOW_FIXTURE,),
    name="CPSkinWorkflow:Integration")
