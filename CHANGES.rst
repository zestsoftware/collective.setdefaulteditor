Changelog
=========

1.5 (2013-09-13)
----------------

- Split the form in two for clarity: one for setting the default
  editor that is used when the member has not set a preference and one
  for setting the editor in the preferences of each existing user.
  [maurits]

- When first loading the form, select the site default editor or the
  default member editor.
  [maurits]


1.4 (2012-11-23)
----------------

- Be smarter about getting all users, also when many_users is true and
  you are using ldap.
  [maurits]

- Use the default_editor site property when it is there (Plone 4).
  [maurits]


1.3 (2012-10-27)
----------------

- Avoid hard dependency on zope.app.component, to gain Plone 4.3
  compatibility.
  [maurits]

- Make compatible with Plone 4.1+ (load CMFCore zcml for the
  permissions).
  [maurits]

- Code moved to https://github.com/zestsoftware/collective.setdefaulteditor
  [maurits]


1.2 (2010-04-27)
----------------

- When there are many users (site_properties/many_users) try to get
  all members by searching for a login with 'a', then 'b', etc.  Not
  ideal, but if for example LDAP gives problems because it returns too
  many results (which means it does not actually return anything) then
  this may help.
  [maurits]


1.1 (2010-04-21)
----------------

- Also offer option to set the chosen editor as new default in
  portal_memberdata.
  [maurits]

- Added form to make setting the editor more user friendly.
  [maurits]

- Check that the input for the wanted editor is sane: is that editor
  actually installed?
  [maurits]


1.0 (2010-03-17)
----------------

- Initial release
  [maurits]
