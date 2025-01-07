# -*- coding: utf-8; -*-
################################################################################
#
#  Sideshow -- Case/Special Order Tracker
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Sideshow.
#
#  Sideshow is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Sideshow is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Sideshow.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data models for Customers
"""

import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from wuttjamaican.db import model

from sideshow.enum import PendingCustomerStatus


class PendingCustomer(model.Base):
    """
    A "pending" customer record, used when entering an :term:`order`
    for new/unknown customer.
    """
    __tablename__ = 'sideshow_pending_customer'

    uuid = model.uuid_column()

    customer_id = sa.Column(sa.String(length=20), nullable=True, doc="""
    ID of the proper customer account associated with this record, if
    applicable.
    """)

    full_name = sa.Column(sa.String(length=100), nullable=True, doc="""
    Full display name for the customer account.
    """)

    first_name = sa.Column(sa.String(length=50), nullable=True, doc="""
    First name of the customer.
    """)

    last_name = sa.Column(sa.String(length=50), nullable=True, doc="""
    Last name of the customer.
    """)

    phone_number = sa.Column(sa.String(length=20), nullable=True, doc="""
    Phone number for the customer.
    """)

    email_address = sa.Column(sa.String(length=255), nullable=True, doc="""
    Email address for the customer.
    """)

    status = sa.Column(sa.Enum(PendingCustomerStatus), nullable=False, doc="""
    Status code for the customer record.
    """)

    created = sa.Column(sa.DateTime(timezone=True), nullable=False,
                        default=datetime.datetime.now, doc="""
    Timestamp when the customer record was created.
    """)

    created_by_uuid = model.uuid_fk_column('user.uuid', nullable=False)
    created_by = orm.relationship(
        model.User,
        cascade_backrefs=False,
        doc="""
        Reference to the
        :class:`~wuttjamaican:wuttjamaican.db.model.auth.User` who
        created the customer record.
        """)

    orders = orm.relationship(
        'Order',
        order_by='Order.order_id.desc()',
        cascade_backrefs=False,
        back_populates='pending_customer',
        doc="""
        List of :class:`~sideshow.db.model.orders.Order` records
        associated with this customer.
        """)

    new_order_batches = orm.relationship(
        'NewOrderBatch',
        order_by='NewOrderBatch.id.desc()',
        cascade_backrefs=False,
        back_populates='pending_customer',
        doc="""
        List of
        :class:`~sideshow.db.model.batch.neworder.NewOrderBatch`
        records associated with this customer.
        """)

    def __str__(self):
        return self.full_name or ""
