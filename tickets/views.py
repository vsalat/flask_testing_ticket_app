# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function)

from flask_apispec import (use_kwargs, marshal_with, MethodResource, doc)

import tickets.models as mdl
from .schemas import (UpdateTicketSchema, AddTicketSchema)


@doc(tags=['ticket'], description='tickets methods')
class TicketResource(MethodResource):

    def get(self, ticket_id):
        ticket = mdl.get_ticket(ticket_id)
        return dict(data=ticket)

    @use_kwargs(UpdateTicketSchema(strict=True))
    def put(self, **data):
        ticket_id = mdl.update_ticket(**data)
        ticket = mdl.get_ticket(ticket_id)
        return dict(data=ticket)


    @use_kwargs(AddTicketSchema(strict=True))
    def post(self, **data):
        ticket_id = mdl.add_ticket(**data)
        ticket = mdl.get_ticket(ticket_id)
        return dict(data=ticket)