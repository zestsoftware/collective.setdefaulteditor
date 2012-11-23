Introduction
============

When you install a new visual editor in your Plone 3 Site, you can set
``wysiwyg_editor`` in portal_memberdata to the proper value for this
new editor.  This only means that *new* users will get this new editor.
To change the editor for all existing users, use this package.

In Plone 4 this should be less necessary, because this Plone version
introduces an option for members to simply use whatever the current
default editor of the site is.  If you migrate from Plone 3 you can
still use this package to change all members so they use this option.

This package makes available a browser view ``@@set-default-editor``
to change the editor setting of members.  Follow the instructions
there.  This has slightly different functionality for Plone 3 and
Plone 4.  You can choose to run this in dry-run mode and see how many
users would be changed.  When dry run is not selected, details are
logged to the instance log.

On the same form you can also select to set the default editor for
new users (Plone 3) or set the editor that is used when 'Use site
default' is selected (Plone 4).


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
