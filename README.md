# Events Django Application

Events-Django-App is an application that provides a database of events in the user's area. Application is splited for3 parts: core, users and tickets.

**Core** part provides the events catalog and related models for user. Addltionally has a system of sending emails to users with Celery.
**Users** includes a authorization system and extends default Django User model.
**Tickets** is very easy selling tickets system. By default events are free for everybody but there is an option to set 'is_free'=False. Then user has to provides a ticket file that will be selling for clients. That part generates a new ticket with unique QR code and send it to user's email.

## Technology Stack
- Django
- Django-Rest-Framework
- Postgres
- Postgis
- Celery

### dev
- Poetry
- Docker
- Pytest
- Precommit
- Black
- Pyright
- Pylint

# How to install

In order to install the application you need to install Poetry and Docker.
Once they are installed, run command 'poetry install'

# How to run

You can run an app in dev mode with command 'poetry run dev'

# How to test

You can test an app in dev mode with command 'poetry run test'

# Note

You don't need to setup any database since both dev and test environments work in Docker. When it comes to production env, you need to set connection up in 'backend/settings/prod.py'
