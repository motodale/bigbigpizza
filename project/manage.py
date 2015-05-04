#!/usr/bin/env python
from flask.ext.script import Manager, Shell, Server
from pizza import app

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.run()
