Changelog
=========

3.0.1 (2015-12-16)
------------------

* Returning ``?form.userId={id}`` to the end of the *Change* link
  for a group when the *Change email settings* page is being
  viewed by someone with the ``Manager`` role
* Fixing the capitalisation of the menu item

3.0.0 (2015-12-08)
------------------

* Adding buttons for people that use touch-screens (which have
  difficulty with drag-and-drop)
* Making the drag-and-drop support more interactive
* Switching the *Add* form to a static form that is always shown
  from a Twitter Bootstrap dialog
* Explaining the different types of address
* Adding `i18n support`_
* Splitting the form into six JSON endpoints
* Splitting the page-template for the group-settings off from the
  main page
* Switching to self-contained JavaScript (ES5) code, which works
  without jQuery or jQuery UI

.. _i18n support:
   https://www.transifex.com/projects/p/gs-profile-email-settings/

2.3.1 (2015-01-08)
------------------

* Updating the ``README.rst`` and setup to point to GitHub_
* Fixing an XML error with the Settings page template, with
  `thanks to Shayne Smith`_

.. _GitHub: https://github.com/groupserver/gs.profile.email.settings
.. _thanks to Shayne Smith: http://groupserver.org/r/post/2NSogtNlD1KlMrJs6JOuTD

2.3.0 (2014-06-04)
------------------

* Use the new ``gs.group.member.email.base`` code

2.2.0 (2014-04-07)
------------------

* Raising errors rather that relying on assert-statements

2.1.0 (2014-03-21)
------------------

* Using a minified JavaScript file
* Switch to Unicode literals

2.0.1 (2013-06-04)
------------------

* Removing some bad JavaScript
* Adding more Twitter Bootstrap

2.0.0 (2013-05-31)
-------------------

* Support the new UI, with breadcrumbs, Twitter Bootstrap
  classes, and no profile-menu and relative URLs
* Refactor of the JavaScript
* Splitting ``setup.py`` in three

1.3.1 (2012-08-29)
------------------

* Stop over-polling

1.3.0 (2012-02-09)
------------------

* Use the new ``send_verification`` method

1.2.1 (2011-06-02)
------------------

* Deleting some commas to make IE7 happy

1.2.0 (2011-04-07)
------------------

* Added to the help
* Handling the case of one unverified email-address
* Adding the page to the *Profile* menu
* Moving the JavaScript to a separate file

1.1.0 (2011-02-23)
------------------

* Drag and drop working
* Remove email address working
* AJAX checking of the unverified email address


1.0.0 (2011-02-04)
------------------

* Initial version
