# gsi_project
Our GSI project for the Silicon Valley pitch.

## current
The current version is using Python, with Bottle web microframework and MySQL (PyMySQL), for the sake of productivity.  It has:
* Dynamic routing
* Encrypted cookies
* Static file serving
* A primitive template format (to be replaced by Bottle's built-in template capabilities when more time is available)
* Account creation and logins
* Set account roles (user/admin/superuser) with a dummy admin panel

## next
The next step is to create a quiz format and the ability to add questions through the admin panel.  For users,
it will display quizzes and list their previous scores.
Probably after the declared deadline 11/31, I will be adding one-page functionality (mainly client-side code) for everything
except POST requests.

## files and versioning
* main.py contains the routes and executes the application
* functions.py contains the functions (e.g. checking logins)
* conf.py contains configuration information such as SQL login information and cookie encryption keys
* static/ contains static files
* templates/ contains template files (*.tmpl indicates an HTML template)

The version for backup branches (backup-*) is: yyyy.mm.dd[.hh], with hours added if there are multiple backups on the same day.
E.g. backup-2015.11.28.17 indicates the backup made on November 28, 2015, at 17:00 hours.
