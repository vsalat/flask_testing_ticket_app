# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function)

import json
from psycopg2.extras import DictCursor
import datetime as dt

from flask import current_app as app


def get_ticket(ticket_id):
    with app.db.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT id, status, create_date, update_date, subject, message, comments from tickets where id=%(ticket_id)s;', dict(ticket_id=ticket_id))
        item = cur.fetchone()
        data = {key: value for key, value in item.iteritems()}
        return data


def add_ticket(email=None, subject=None, message=None):
    with app.db.cursor() as cur:
        create_datetime = dt.datetime.now()
        query = cur.execute(
            'INSERT into tickets (create_date, subject, message, email) values \
            (%(create_date)s, %(subject)s, %(message)s, %(email)s) RETURNING id;',
            dict(create_date=create_datetime, subject=subject, message=message, email=email)
        )
        ticket_id = cur.fetchone()[0]
        app.db.commit()
        return ticket_id


def update_ticket(ticket_id, email=None, action=None, body=None):
    with app.db.cursor() as cur:
        update_datetime = dt.datetime.utcnow()
        comment = json.dumps(dict(create_date=update_datetime.isoformat(), email=email, body=body))
        query = cur.execute(
            'UPDATE tickets SET status=(%s), update_date=(%s), comments=comments ||(%s) where tickets.id=(%s)',
            (action, update_datetime, comment, ticket_id)
        )
        app.db.commit()
        return ticket_id