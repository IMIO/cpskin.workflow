def installWorkflows(context):
    if context.readDataFile('cpskin.workflow-default.txt') is None:
        return
    #XXX To be completed (default workflow & changeStateCriteria)


def uninstallWorkflows(context):
    if context.readDataFile('cpskin.workflow-uninstall.txt') is None:
        return
    #XXX To be completed (changeStateCriteria)
