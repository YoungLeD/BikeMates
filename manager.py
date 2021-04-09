#!/usr/bin/env python
from flask_script import Manager, Server
from app import models
from app import app, db

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


@manager.shell
def make_shell_context():
    return dict(app=app, models=models)


def fill_samples():
    from datetime import datetime
    # User
    user = models.User('Test', 'abc@example.com', '1234567890')
    db.session.add(user)
    db.session.commit()

    # Events

    event1 = models.Event(1, 'sample event 1', datetime.now().timestamp(), [55.74, 37.61], 'description 1')
    event2 = models.Event(1, 'sample event 2', datetime.now().timestamp(), [55.75, 37.63], 'description 2')
    event3 = models.Event(1, 'sample event 3', datetime.now().timestamp(), [55.75, 37.61], 'description 3')
    event4 = models.Event(1, 'sample event 4', datetime.now().timestamp(), [55.74, 37.63], 'description 4')
    for e in (event1, event2, event3, event4):
        db.session.add(e)
    db.session.commit()

    # Route
    route = models.Route(1, 'sample route', 'route description')
    db.session.add(route)
    db.session.commit()
    point1 = models.Point([55.74, 37.61], route.id)
    point2 = models.Point([55.75, 37.61], route.id)
    point3 = models.Point([55.75, 37.63], route.id)
    point4 = models.Point([55.74, 37.63], route.id)
    for p in (point1, point2, point3, point4):
        db.session.add(p)

    route.set_points([point1, point2, point3, point4])
    db.session.add(route)

    db.session.commit()


@manager.command
def initdb():
    db.create_all()
    fill_samples()


if __name__ == "__main__":
    manager.run()
