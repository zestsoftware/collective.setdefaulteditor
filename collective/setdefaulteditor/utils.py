import logging
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

logger = logging.getLogger('collective.setdefaulteditor')


def set_editor_for_all(wanted_editor, dry_run=False):
    """Set the wanted editor for all users.

    When dry_run is True, we do not change anything.

    Return a count for number of users who remain the same, and number
    of users who have changed (or will change).
    """
    site = getSite()
    pm = getToolByName(site, 'portal_membership')
    same = 0
    changed = 0
    logger.info("Updating editor for all members.")
    if dry_run:
        logger.info("Dry-run selected, not changing anything.")

    # We could use pm.getMemberIds, but that does not find e.g. LDAP users.
    for plone_user in pm.searchForMembers():
        member_id = plone_user.getId()
        member = pm.getMemberById(member_id)
        editor = member.getProperty('wysiwyg_editor', None)
        if editor == wanted_editor:
            msg = '%s: %s already selected, leaving alone.' % (
                member_id, wanted_editor)
            same += 1
        else:
            msg = '%s: setting %s as default editor.' % (
                member_id, wanted_editor)
            if not dry_run:
                member.setMemberProperties({'wysiwyg_editor': wanted_editor})
            changed += 1
        if dry_run:
            logger.debug(msg)
        else:
            logger.info(msg)

    return (same, changed)
