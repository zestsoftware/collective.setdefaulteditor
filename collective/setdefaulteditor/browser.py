from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from collective.setdefaulteditor.utils import set_editor_for_all


class SetEditor(BrowserView):

    def __call__(self):
        wanted_editor = self.request.get('editor')
        if not wanted_editor:
            return "Call with for example '?editor=TinyMCE&dryrun=1'"
        context = aq_inner(self.context)
        pprops = getToolByName(context, 'portal_properties')
        available = pprops.site_properties.available_editors
        if wanted_editor not in available:
            return "%r is not available as editor. Choose one of %r." % (
                wanted_editor, available)
        dry_run = int(self.request.get('dryrun', 0))
        dry_run = bool(dry_run)
        same, changed = set_editor_for_all(wanted_editor, dry_run=dry_run)
        msg = "Done. %d were the same; %d changed." % (same, changed)
        if dry_run:
            msg += ' Dry-run selected: nothing changed.'
        return msg
