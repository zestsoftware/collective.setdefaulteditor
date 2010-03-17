Introduction
============

When you install a new visual editor in your Plone Site, you can set
``wysiwyg_editor`` in portal_memberdata to the proper value for this
new editor.  This only means that new users will get this new editor.
To change the editor for all existing users, use this package.

This makes available a browser view ``@@set-default-editor``.  Call
this to get some simple instructions in plain text about how to edit
the url to do something useful (patches for making a simple front-end
template for this are welcome).

Call for example
``<plone_site_url>/@@set-default-editor?editor=TinyMCE&dryrun=1`` to
run this in dry-run mode and see how many users would be changed.  See
the instance log for details.  Remove the dryrun option (or set it to
``0``) to really set the editor.


Todo
====

- Create a template so the user can just click instead of having to edit the URL.

- Check that the input for the wanted editor is sane: is that editor actually installed?

- Also set the editor as new default in portal_memberdata.

- Add tests.


