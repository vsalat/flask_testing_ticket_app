# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function)
from apispec import APISpec

APPLICATION_ROOT = '/api'
DATABASE = 'ticket_database'
DATABASE_USER = 'ticket_user'
DATABASE_PASSWORD = 'qwerty'
DATABASE_HOST = 'localhost'

APISPEC_SPEC = APISpec(
        title='tickets application',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    )
