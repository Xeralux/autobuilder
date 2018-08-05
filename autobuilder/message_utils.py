from buildbot.reporters.message import MessageFormatter
from twisted.internet import defer


# noinspection PyPep8Naming
@defer.inlineCallbacks
def getChangesForSourceStamps(master, sslist):
    changelist = []
    for ss in sslist:
        changesd = master.data.get(("sourcestamps", ss['ssid'], "changes"))
        sourcestampd = master.data.get(("sourcestamps", ss['ssid']))
        changes, sourcestamp = yield defer.gatherResults([changesd, sourcestampd])
        for c in changes:
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
        if ctx['sourcestamps']:
            ctx['changes'] = getChangesForSourceStamps(master, ctx['buildset']['sourcestamps'])
        else:
            ctx['changes'] = []

