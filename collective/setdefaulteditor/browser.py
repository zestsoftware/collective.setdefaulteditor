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
        marker = object()
        context = aq_inner(self.context)
        pprops = getToolByName(context, 'portal_properties')
        site_props = pprops.site_properties
        self.available_editors = list(site_props.available_editors)
        site_default_editor = site_props.getProperty('default_editor', marker)
        # Add empty string for using site default.
        if site_default_editor is not marker:
            self.available_editors.append('')
        md = getToolByName(context, 'portal_memberdata')
        self.default_editor = md.getProperty('wysiwyg_editor', 'None')

        wanted_editor = self.request.get('editor', marker)
        if wanted_editor is marker:
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
        logger.info(msg)
        if dry_run:
            msg = 'Dry-run selected: nothing changed.'
            status.addStatusMessage(msg, type='warning')
            logger.info(msg)
            return

        if self.request.get('update-default'):
            if wanted_editor == '':
                msg = "Cannot set wysiwyg_editor for new members to nothing."
                logger.warn(msg)
                status.addStatusMessage(msg, type='warn')
            else:
                if site_default_editor is marker:
                    # Plone 3, usually.
                    md._updateProperty('wysiwyg_editor', wanted_editor)
                    msg = "Updated wysiwyg_editor for new members to %r" % (
                        wanted_editor)
                else:
                    site_props._updateProperty('default_editor', wanted_editor)
                    md._updateProperty('wysiwyg_editor', '')
                    msg = "Updated default wysiwyg_editor to %r. New members will use the site default." % (
                        wanted_editor)
                logger.info(msg)
                status.addStatusMessage(msg, type='info')
