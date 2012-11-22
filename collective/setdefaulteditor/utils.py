import logging
from Products.CMFCore.utils import getToolByName
try:
    from zope.component.hooks import getSite
    getSite  # pyflakes
except ImportError:
    from zope.app.component.hooks import getSite

logger = logging.getLogger('collective.setdefaulteditor')


def get_all_userids():
    """Get all users.

    Note that we could use pm.getMemberIds, but that does not find
    e.g. LDAP users.

    Also, we want to take into account that there may be many users,
    which in the case of LDAP means you get no results back or get an
    error.  So in that case we do more specific searches.  But there
    does not seem to be a way search for 'a*'.  Simply searching for
    'a' returns everyone with an 'a' somewhere in the login, which is
    not what we want.  Seems we need to do just that and do some extra
    filtering.

    Actually, using pas.searchUsers works too.  In a standard Plone
    site this will list all users from source_users and
    mutable_properties.  If you add ldap then you will get users from
    there as well, which could return an empty list if there are too
    many users.  But we have the users from mutable_properties, which
    are the ones we are actually going to change.

    We just need to filter out duplicate ones.
    """
    site = getSite()
    pas = getToolByName(site, 'acl_users')
    return set([user.get('id') for user in pas.searchUsers()])


def set_editor_for_all(wanted_editor, dry_run=False):
    """Set the wanted editor for all users.

    When dry_run is True, we do not change anything.

    Return a count for number of users who remain the same, and number
    of users who have changed (or will change).

    Note that we could be tempted to change the data in
    mutable_properties._storage directly, but the data not only lives
    there but also in separate user property sheets.  So that is not advisable.
    """
    site = getSite()
    pm = getToolByName(site, 'portal_membership')
    same = 0
    changed = 0
    if wanted_editor is None:
        # Not to be confused with the string 'None' meaning a basic textarea.
        wanted_editor = ''
    logger.info("Updating editor for all members to %r.", wanted_editor)
    if dry_run:
        logger.info("Dry-run selected, not changing anything.")

    for member_id in get_all_userids():
        member = pm.getMemberById(member_id)
        if not member:
            # Might be in ldap but not in Plone (yet).
            logger.info("Member id %r not found.", member_id)
            continue
        editor = member.getProperty('wysiwyg_editor', None)
        if editor == wanted_editor:
            msg = '%s: %r already selected, leaving alone.' % (
                member_id, wanted_editor)
            same += 1
        else:
            msg = '%s: setting %r as default editor.' % (
                member_id, wanted_editor)
            if not dry_run:
                member.setMemberProperties({'wysiwyg_editor': wanted_editor})
            changed += 1
        if dry_run:
            logger.debug(msg)
        else:
            logger.info(msg)

    return (same, changed)
