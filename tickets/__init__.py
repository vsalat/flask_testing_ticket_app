# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function)

import psycopg2
from flask import Flask
from apispec import APISpec
from flask_apispec import FlaskApiSpec

docs = FlaskApiSpec()
def create_app(config_filename):
    """
    Flask application factory
    :param config_filename:
    :return:
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    spec = APISpec(
        title='Swagger TicketSystem',
        version='1.0.0',
        plugins=[
            'apispec.ext.flask',
            'apispec.ext.marshmallow',
        ],
    )
    app.db = psycopg2.connect("dbname='{db_name}' user='{db_user}' password='{db_password}' host='{db_host}'".format(
        db_name=app.config['DATABASE'],
        db_user=app.config['DATABASE_USER'],
        db_password=app.config['DATABASE_PASSWORD'],
        db_host=app.config['DATABASE_HOST']
    ))
    docs.init_app(app)
    from tickets.views import TicketResource
    app.add_url_rule('/ticket/<int:ticket_id>', view_func=TicketResource.as_view('TicketResourceId'), methods=['get',
                                                                                                              'put'])
    app.add_url_rule('/ticket', view_func=TicketResource.as_view('TicketResource'), methods=['POST'])

    docs.register(TicketResource, endpoint='TicketResourceId')
    docs.register(TicketResource, endpoint='TicketResource')
    return app
