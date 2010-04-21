import logging
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from collective.setdefaulteditor.utils import set_editor_for_all

logger = logging.getLogger('collective.setdefaulteditor')


class SetEditor(BrowserView):

    def __call__(self):
        self.update()
        # Render whatever was set as the template in zcml:
        return self.index()

    def update(self):
        """Apply settings and update some variables on this view.
        """
        context = aq_inner(self.context)
        pprops = getToolByName(context, 'portal_properties')
        self.available_editors = pprops.site_properties.available_editors
        md = getToolByName(context, 'portal_memberdata')
        self.default_editor = md.getProperty('wysiwyg_editor', 'None')

        wanted_editor = self.request.get('editor')
        if not wanted_editor:
            # nothing to do
            return

        status = IStatusMessage(self.request)
        if wanted_editor not in self.available_editors:
            msg = "%r is not available as editor. Choose one of %r." % (
                wanted_editor, self.available_editors)
            status.addStatusMessage(msg, type='error')
            return

        dry_run = (self.request.get('dryrun', 'off') == 'on')
        same, changed = set_editor_for_all(wanted_editor, dry_run=dry_run)
        msg = "Done. %d were the same; %d needed changing." % (same, changed)
        status.addStatusMessage(msg, type='info')
        if dry_run:
            msg = 'Dry-run selected: nothing changed.'
            status.addStatusMessage(msg, type='warning')
            return

        if self.request.get('update-default'):
            md._updateProperty('wysiwyg_editor', wanted_editor)
            msg = "Updated wysiwyg_editor for new members to %r" % (
                wanted_editor)
            logger.info(msg)
            status.addStatusMessage(msg, type='info')
