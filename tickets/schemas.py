# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function)

from flask import request
from marshmallow import (Schema, fields, post_load, validate, ValidationError)

from .constants import (CLOSE, OPEN, ANSWER, WAIT)
import tickets.models as mdl


class CommentTicketSchema(Schema):
    email = fields.Email(required=True)
    body = fields.String(required=True)


class UpdateTicketSchema(Schema):
    status = fields.String(validate=validate.OneOf([WAIT, ANSWER, CLOSE]), required=True)
    comment = fields.Nested(CommentTicketSchema, required=True)

    @post_load
    def _validate(self, data):
        ticket_id = request.view_args.get('ticket_id')
        status = data.get('status')
        if status == OPEN:
            raise ValidationError(u'Неправильный status', ['status'])

        ticket_object = mdl.get_ticket(ticket_id)

        if not ticket_object:
            raise ValidationError(u'Указанный тикет не найден', ['ticket_id'])

        ticket_status = ticket_object[1]
        if ticket_status == OPEN and status not in [ANSWER, CLOSE]:
            raise ValidationError(u'На тикет можно либо отвеить, либо закрыть', ['status'])

        if ticket_status == ANSWER and status not in [WAIT, CLOSE]:
            raise ValidationError(u'Тикет можно перевести в статус "ожидае ответа" или "закрыт"', ['status'])

        if ticket_status == CLOSE:
            raise ValidationError(u'Тике уже закрыт изменить его нельзя', ['status'])
        comment = data['comment']
        return dict(ticket_id=ticket_id, email=comment.get('email'), status=status, body=comment.get('body'))


class AddTicketSchema(Schema):
    message = fields.String(required=True)
    subject = fields.String(validate=validate.Length(min=1, max=40))
    email = fields.Email(required=True)

    @post_load
    def _validate(self, data):
        return dict(email=data.get('email'), subject=data.get('subject'), message=data.get('message'))


