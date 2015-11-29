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
* Graded quiz capability

## next
The next step is to associate quiz scores with accounts so you can view your average score.
After that I'll make an admin panel so we can create and add questions to quizzes without fiddling with the database.  (This will also allow me to SQL-sanitize quiz-related queries).
Then I'll add a one-page design for all the GET requests.  Entirely front-end there.
The final step will be styling.

## files and versioning
* main.py contains the routes and executes the application
* functions.py contains the functions (e.g. checking logins)
* conf.py contains configuration information such as SQL login information and cookie encryption keys
* static/ contains static files
* templates/ contains template files (*.tmpl indicates an HTML template)

The version for backup branches (backup-*) is: yyyy.mm.dd[.hh], with hours added if there are multiple backups on the same day.
E.g. backup-2015.11.28.17 indicates the backup made on November 28, 2015, at 17:00 hours.

## notes
* Regarding NodeJS performance: https://www.quora.com/How-does-FreeCodeCamp-pay-for-servers/answer/Quincy-Larson/comment/14511154?__snids__=1444527384&__nsrc__=4#comment14511698
I'm fairly confident that guy knows about JavaScript; he's behind FreeCodeCamp.  Which teaches JavaScript.
