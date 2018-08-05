from buildbot.reporters.message import MessageFormatter
from twisted.internet import defer
from twisted.python import log


# noinspection PyPep8Naming
@defer.inlineCallbacks
def getChangesForSourceStamps(master, sslist):
    log.msg("getChangesForSourceStamps: sslist=%s" % sslist)
    changelist = []
    for ss in sslist:
        log.msg('SOURCESTAMP: %s' % ss)
        changesd = master.data.get(("sourcestamps", ss['ssid'], "changes"))
        sourcestampd = master.data.get(("sourcestamps", ss['ssid']))
        changes, sourcestamp = yield defer.gatherResults([changesd, sourcestampd])
        log.msg("For ssid %s, changes=%s, sourcestamp=%s" % (ss['ssid'], changes, sourcestamp))
        for c in changes:
            log.msg('CHANGE: %s' % c)
            change = {'author': c['author'],
                      'comments': c['comments'],
                      'revlink': c['revlink'],
                      'revision': ss['revision']
                      }
            changelist.append(change)
    defer.returnValue(changelist)


class AutobuilderMessageFormatter(MessageFormatter):
    def buildAdditionalContext(self, master, ctx):
        ctx.update(self.ctx)
        log.msg("buildAdditionalContext: orig context=%s" % ctx)
        if ctx['sourcestamps']:
            ctx['changes'] = getChangesForSourceStamps(master, ctx['buildset']['sourcestamps'])
        else:
            ctx['changes'] = []
        log.msg("buildAdditionalContext: set changes to: %s" % ctx['changes'])

