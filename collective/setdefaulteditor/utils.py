import logging
import string
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

logger = logging.getLogger('collective.setdefaulteditor')


def get_all_users():
    """Get all users.

    Note that we could use pm.getMemberIds, but that does not find
    e.g. LDAP users.

    Also, we want to take into account that there may be many users,
    which in the case of LDAP means you get no results back or get an
    error.  so in that case we do more specific searches.  But there
    does not seem to be a way search for 'a*'.  Simply searching for
    'a' returns everyone with an 'a' somewhere in the login, which is
    not what we want.  Seems we need to do just that and do some extra
    filtering.

    """
    site = getSite()
    pm = getToolByName(site, 'portal_membership')
    pp = getToolByName(site, 'portal_properties')
    many_users = pp.site_properties.getProperty('many_users', False)

    if not many_users:
        for plone_user in pm.searchForMembers():
            yield plone_user
    else:
        logger.info("Many users: splitting search into multiple queries.")
        found = []
        for char in string.ascii_letters:
            logger.debug("Searching for %r", char)
            for plone_user in pm.searchForMembers(login=char):
                user_id = plone_user.getId()
                if user_id not in found:
                    logger.debug("Found %s", user_id)
                    found.append(user_id)
                    yield plone_user


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

    for plone_user in get_all_users():
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
