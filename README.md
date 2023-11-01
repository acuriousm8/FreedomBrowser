# FreedomBrowser

A basic Python tabbed browser using the PyQt5 framework. Includes some basic web browser things like a very rudimental bookmark system, context menus, multiwindow support, window snapping support, and download support. It was designed to be portable to allow it to be run in public spaces. Includes three methods for bypassing website restrictions.

## Custom Functions
* Web restriction bypasses
  * The `eye button` in the toolbar automatically runs the current site through Google Translate.
  * The `Ignore Errors` option in the side menu can also be used to bypass certain website restrictions.
  * It also ignores any certificates on the system that may attempt to enforce blocks (like securely).
* Brainly Mode (broken)
  * Brainly mode is meant to bypass the advertising requirements to allow unlimited Brainly questions without signing in or watching ads
  * They recently patched the method I used to bypass it, which will need updating.
 
## To Do
* Take out the discord tokens from the authentication system so I can upload the system here.
* Store bookmarks locally and persistently.
* Make a proper download menu rather than the rudimentary one included.
* Port to pyside6 to allow Mac (Mx processors series included) and Linux usage (mostly done).
* Fix Brainly mode or remove it if it's no longer possible.
* Make a settings menu.
* Other quality-of-life improvements

## Status
I probably won't be updating this much as I made it to bypass school blocks in high school. I'm no longer in high school, and it has thus served its purpose.
