#!/usr/bin/env python2.7

import buzzwebpanel
from buzzwebpanel import db
import buzzwebpanel.models

import flask_script
import flask_migrate

manager = flask_script.Manager(buzzwebpanel.app)

# Database migrations
migrate = flask_migrate.Migrate(buzzwebpanel.app, buzzwebpanel.db)
manager.add_command('db', flask_migrate.MigrateCommand)


if __name__ == '__main__':
    manager.run()