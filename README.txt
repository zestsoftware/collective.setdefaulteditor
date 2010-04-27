Introduction
============

When you install a new visual editor in your Plone Site, you can set
``wysiwyg_editor`` in portal_memberdata to the proper value for this
new editor.  This only means that *new* users will get this new editor.
To change the editor for all existing users, use this package.

This makes available a browser view ``@@set-default-editor`` and
follow the instructions.  You can choose to run this in dry-run mode
and see how many users would be changed.  When dry run is not
selected, details are logged to the instance log.

On the same form you can also select to set the default editor for
*new* users at the same time as changing it for existing users.


Many users
==========

When there are many users (see Site Setup / Users and Groups /
Settings) we try to get all members by searching for a login with 'a',
then 'b', etc.  This is not ideal, but if for example LDAP gives
problems because it returns too many results (which means it does not
actually return anything at all) then this may help.  If you still
have trouble, try setting ``event-log-level = debug`` in the
``instance`` section of your ``buildout.cfg``, run buildout again,
start the instance in the foreground and then try again and see where
it goes wrong.  Hopefully this gives you an idea for some custom code
to write.  (If it is general enough, please share your work in a
branch and contact me.)


Todo
====

- Add tests.


Contributors
============

I (Maurits van Rees) found the main code in an article_ by Rob
Gietema.  He apparently got the script from Kelly Craig.  And I have
seen the same code in a post_ to the plone-setup list by Reinout van
Rees.  So I claim it back in defense of our family honour. ;-)

.. _article: http://plone.org/products/tinymce/documentation/how-to/how-to-set-tinymce-as-default-editor-for-current-users/
.. _post: http://www.mail-archive.com/setup@lists.plone.org/msg01414.html
