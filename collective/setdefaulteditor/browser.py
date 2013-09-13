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
        site_props = pprops.site_properties

        # Determine the wanted editor.
        wanted_editor = self.request.get('editor', marker)

        # What are the defaults?
        self.site_default_editor = site_props.getProperty('default_editor')
        self.member_default_editor = md.getProperty('wysiwyg_editor')

        # Get possible editors.
        editors = list(site_props.getProperty('available_editors', []))
        if self.site_default_editor and '' not in editors:
            # Plone 4.  A site default is supported, so add an empty
            # string for using this.
            editors.append('')

        # Gather display information about the editors.
        self.available_editors = []
        if wanted_editor is marker:
            selected_editor = self.site_default_editor or self.member_default_editor
        else:
            selected_editor = wanted_editor
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
            if editor == selected_editor:
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

        # Is this a dry run or are we allowed to change things?
        dry_run = (self.request.get('dryrun', 'off') == 'on')

        # Change the editor for all members.
        if self.request.get('update-user'):
            same, changed = set_editor_for_all(wanted_editor, dry_run=dry_run)
            msg = "Done. %d were the same; %d needed changing." % (
                same, changed)
            status.addStatusMessage(msg, type='info')
            logger.info(msg)

        # Update the default editor.
        if self.request.get('update-default'):
            if wanted_editor == '':
                msg = ("Cannot set the default wysiwyg_editor to the site "
                       "default.")
                logger.warn(msg)
                status.addStatusMessage(msg, type='warning')
            else:
                if self.site_default_editor is None:
                    # Plone 3, usually.
                    if not dry_run:
                        md._updateProperty('wysiwyg_editor', wanted_editor)
                        self.member_default_editor = wanted_editor
                    msg = "Updated wysiwyg_editor for new members to %r" % (
                        wanted_editor)
                else:
                    if not dry_run:
                        site_props._updateProperty(
                            'default_editor', wanted_editor)
                        self.site_default_editor = wanted_editor
                        md._updateProperty('wysiwyg_editor', '')
                        self.member_default_editor = ''
                    msg = ("Updated default wysiwyg_editor to %r. New members "
                           "will use the site default." % (wanted_editor))
                logger.info(msg)
                status.addStatusMessage(msg, type='info')

        if dry_run:
            msg = 'Dry-run selected: nothing changed.'
            status.addStatusMessage(msg, type='warning')
            logger.info(msg)
            return
