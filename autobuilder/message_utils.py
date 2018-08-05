from buildbot.reporters.message import MessageFormatter
from twisted.internet import defer
from twisted.python import log


def getChangesForSourceStamps(master, sslist):
    log.msg("getChangesForSourceStamps: sslist=%s" % sslist)
    changelist = []
    for ss in sslist:
        log.msg('SOURCESTAMP: %s' % ss)
        changes = master.data.get(("sourcestamps", ss['ssid'], "changes"))
        log.msg('CHANGES: %s' % changes)
        changelist += changes
    return changelist


class AutobuilderMessageFormatter(MessageFormatter):
    def buildAdditionalContext(self, master, ctx):
        ctx.update(self.ctx)
        log.msg("buildAdditionalContext: orig context=%s" % ctx)
        if ctx['sourcestamps']:
            ctx['changes'] = getChangesForSourceStamps(master, ctx['buildset']['sourcestamps'])
        else:
            ctx['changes'] = []
        log.msg("buildAdditionalContext: set changes to: %s" % ctx['changes'])

