import logging
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.i18nmessageid import MessageFactory

from collective.setdefaulteditor.utils import set_editor_for_all

logger = logging.getLogger('collective.setdefaulteditor')
#_ = MessageFactory('collective.setdefaulteditor')
PMF = MessageFactory('plone')


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
        md = getToolByName(context, 'portal_memberdata')
        wanted_editor = self.request.get('editor', marker)
        site_props = pprops.site_properties
        site_default_editor = site_props.getProperty('default_editor', marker)
        member_default_editor = md.getProperty('wysiwyg_editor', marker)

        # Determine the default editor.
        if member_default_editor is marker:
            if site_default_editor is marker:
                self.default_editor = 'None'
            else:
                self.default_editor = site_default_editor
        else:
            self.default_editor = member_default_editor

        # Get possible editors.
        editors = list(site_props.getProperty('available_editors', []))
        if '' not in editors:
            # Add empty string for using site default.
            editors.append('')
        self.available_editors = []
        for editor in editors:
            if editor == 'None':
                title = PMF(u"label_ordinary_content_editor",
                            default=(u"Basic HTML textarea editor (works in "
                                     u"all browsers)"))
            elif editor == '':
                title = PMF(u"vocabulary-available-editor-novalue",
                            default=u"Use site default")
            else:
                title = editor
            if editor == wanted_editor:
                selected = 'selected'
            else:
                selected = None
            self.available_editors.append(dict(
                value=editor,
                selected=selected,
                title=title))

        # Only POST requests allowed beyond this point.
        if self.request.get('REQUEST_METHOD') != 'POST':
            return

        # Check the wanted editor.
        if wanted_editor is marker:
            # nothing to do
            return
        status = IStatusMessage(self.request)
        if wanted_editor not in editors:
            msg = "%r is not available as editor. Choose one of %r." % (
                wanted_editor, editors)
            status.addStatusMessage(msg, type='error')
            return

        # Change the editor for all members.
        dry_run = (self.request.get('dryrun', 'off') == 'on')
        same, changed = set_editor_for_all(wanted_editor, dry_run=dry_run)
        msg = "Done. %d were the same; %d needed changing." % (same, changed)
        status.addStatusMessage(msg, type='info')
        logger.info(msg)

        # Update the default editor.
        if self.request.get('update-default'):
            if wanted_editor == '':
                msg = "Cannot set wysiwyg_editor for new members to nothing."
                logger.warn(msg)
                status.addStatusMessage(msg, type='warn')
            else:
                if site_default_editor is marker:
                    # Plone 3, usually.
                    if not dry_run:
                        md._updateProperty('wysiwyg_editor', wanted_editor)
                    msg = "Updated wysiwyg_editor for new members to %r" % (
                        wanted_editor)
                else:
                    if not dry_run:
                        site_props._updateProperty(
                            'default_editor', wanted_editor)
                        md._updateProperty('wysiwyg_editor', '')
                    msg = ("Updated default wysiwyg_editor to %r. New members "
                           "will use the site default." % (wanted_editor))
                logger.info(msg)
                status.addStatusMessage(msg, type='info')

        if dry_run:
            msg = 'Dry-run selected: nothing changed.'
            status.addStatusMessage(msg, type='warning')
            logger.info(msg)
            return
