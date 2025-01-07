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
New Order Batch Handler
"""

import datetime
import decimal

from wuttjamaican.batch import BatchHandler

from sideshow.db.model import NewOrderBatch


class NewOrderBatchHandler(BatchHandler):
    """
    The :term:`batch handler` for New Order Batches.

    This is responsible for business logic around the creation of new
    :term:`orders <order>`.  A
    :class:`~sideshow.db.model.batch.neworder.NewOrderBatch` tracks
    all user input until they "submit" (execute) at which point an
    :class:`~sideshow.db.model.orders.Order` is created.
    """
    model_class = NewOrderBatch

    def set_pending_customer(self, batch, data):
        """
        Set (add or update) pending customer info for the batch.

        This will clear the
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatch.customer_id`
        and set the
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatch.pending_customer`,
        creating a new record if needed.  It then updates the pending
        customer record per the given ``data``.

        :param batch:
           :class:`~sideshow.db.model.batch.neworder.NewOrderBatch`
           to be updated.

        :param data: Dict of field data for the
           :class:`~sideshow.db.model.customers.PendingCustomer`
           record.
        """
        model = self.app.model
        enum = self.app.enum

        # remove customer account if set
        batch.customer_id = None

        # create pending customer if needed
        pending = batch.pending_customer
        if not pending:
            kw = dict(data)
            kw.setdefault('status', enum.PendingCustomerStatus.PENDING)
            pending = model.PendingCustomer(**kw)
            batch.pending_customer = pending

        # update pending customer
        if 'first_name' in data:
            pending.first_name = data['first_name']
        if 'last_name' in data:
            pending.last_name = data['last_name']
        if 'full_name' in data:
            pending.full_name = data['full_name']
        elif 'first_name' in data or 'last_name' in data:
            pending.full_name = self.app.make_full_name(data.get('first_name'),
                                                        data.get('last_name'))
        if 'phone_number' in data:
            pending.phone_number = data['phone_number']
        if 'email_address' in data:
            pending.email_address = data['email_address']

        # update batch per pending customer
        batch.customer_name = pending.full_name
        batch.phone_number = pending.phone_number
        batch.email_address = pending.email_address

    def add_pending_product(self, batch, pending_info,
                            order_qty, order_uom):
        """
        Add a new row to the batch, for the given "pending" product
        and order quantity.

        See also :meth:`set_pending_product()` to update an existing row.

        :param batch:
           :class:`~sideshow.db.model.batch.neworder.NewOrderBatch` to
           which the row should be added.

        :param pending_info: Dict of kwargs to use when constructing a
           new :class:`~sideshow.db.model.products.PendingProduct`.

        :param order_qty: Quantity of the product to be added to the
           order.

        :param order_uom: UOM for the order quantity; must be a code
           from :data:`~sideshow.enum.ORDER_UOM`.

        :returns:
           :class:`~sideshow.db.model.batch.neworder.NewOrderBatchRow`
           which was added to the batch.
        """
        model = self.app.model
        enum = self.app.enum
        session = self.app.get_session(batch)

        # make new pending product
        kw = dict(pending_info)
        kw.setdefault('status', enum.PendingProductStatus.PENDING)
        product = model.PendingProduct(**kw)
        session.add(product)
        session.flush()
        # nb. this may convert float to decimal etc.
        session.refresh(product)

        # make/add new row, w/ pending product
        row = self.make_row(pending_product=product,
                            order_qty=order_qty, order_uom=order_uom)
        self.add_row(batch, row)
        session.add(row)
        session.flush()
        return row

    def set_pending_product(self, row, data):
        """
        Set (add or update) pending product info for the given batch row.

        This will clear the
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.product_id`
        and set the
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.pending_product`,
        creating a new record if needed.  It then updates the pending
        product record per the given ``data``, and finally calls
        :meth:`refresh_row()`.

        Note that this does not update order quantity for the item.

        See also :meth:`add_pending_product()` to add a new row
        instead of updating.

        :param row:
           :class:`~sideshow.db.model.batch.neworder.NewOrderBatchRow`
           to be updated.

        :param data: Dict of field data for the
           :class:`~sideshow.db.model.products.PendingProduct` record.
        """
        model = self.app.model
        enum = self.app.enum
        session = self.app.get_session(row)

        # values for these fields can be used as-is
        simple_fields = [
            'scancode',
            'brand_name',
            'description',
            'size',
            'weighed',
            'department_id',
            'department_name',
            'special_order',
            'vendor_name',
            'vendor_item_code',
            'notes',
            'unit_cost',
            'case_size',
            'case_cost',
            'unit_price_reg',
        ]

        # clear true product id
        row.product_id = None

        # make pending product if needed
        product = row.pending_product
        if not product:
            kw = dict(data)
            kw.setdefault('status', enum.PendingProductStatus.PENDING)
            product = model.PendingProduct(**kw)
            session.add(product)
            row.pending_product = product
            session.flush()

        # update pending product
        for field in simple_fields:
            if field in data:
                setattr(product, field, data[field])

        # nb. this may convert float to decimal etc.
        session.flush()
        session.refresh(product)

        # refresh per new info
        self.refresh_row(row)

    def refresh_row(self, row, now=None):
        """
        Refresh all data for the row.  This is called when adding a
        new row to the batch, or anytime the row is updated (e.g. when
        changing order quantity).

        This calls one of the following to update product-related
        attributes for the row:

        * :meth:`refresh_row_from_pending_product()`
        * :meth:`refresh_row_from_true_product()`

        It then re-calculates the row's
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.total_price`
        and updates the batch accordingly.

        It also sets the row
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.status_code`.
        """
        enum = self.app.enum
        row.status_code = None
        row.status_text = None

        # ensure product
        if not row.product_id and not row.pending_product:
            row.status_code = row.STATUS_MISSING_PRODUCT
            return

        # ensure order qty/uom
        if not row.order_qty or not row.order_uom:
            row.status_code = row.STATUS_MISSING_ORDER_QTY
            return

        # update product attrs on row
        if row.product_id:
            self.refresh_row_from_true_product(row)
        else:
            self.refresh_row_from_pending_product(row)

        # we need to know if total price changes
        old_total = row.total_price

        # update quoted price
        row.unit_price_quoted = None
        row.case_price_quoted = None
        if row.unit_price_sale is not None and (
                not row.sale_ends
                or row.sale_ends > (now or datetime.datetime.now())):
            row.unit_price_quoted = row.unit_price_sale
        else:
            row.unit_price_quoted = row.unit_price_reg
        if row.unit_price_quoted is not None and row.case_size:
            row.case_price_quoted = row.unit_price_quoted * row.case_size

        # update row total price
        row.total_price = None
        if row.order_uom == enum.ORDER_UOM_CASE:
            if row.unit_price_quoted is not None and row.case_size is not None:
                row.total_price = row.unit_price_quoted * row.case_size * row.order_qty
        else: # ORDER_UOM_UNIT (or similar)
            if row.unit_price_quoted is not None:
                row.total_price = row.unit_price_quoted * row.order_qty
        if row.total_price is not None:
            row.total_price = decimal.Decimal(f'{row.total_price:0.2f}')

        # update batch if total price changed
        if row.total_price != old_total:
            batch = row.batch
            batch.total_price = ((batch.total_price or 0)
                                 + (row.total_price or 0)
                                 - (old_total or 0))

        # all ok
        row.status_code = row.STATUS_OK

    def refresh_row_from_pending_product(self, row):
        """
        Update product-related attributes on the row, from its
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.pending_product`
        record.

        This is called automatically from :meth:`refresh_row()`.
        """
        product = row.pending_product

        row.product_scancode = product.scancode
        row.product_brand = product.brand_name
        row.product_description = product.description
        row.product_size = product.size
        row.product_weighed = product.weighed
        row.department_id = product.department_id
        row.department_name = product.department_name
        row.special_order = product.special_order
        row.case_size = product.case_size
        row.unit_cost = product.unit_cost
        row.unit_price_reg = product.unit_price_reg

    def refresh_row_from_true_product(self, row):
        """
        Update product-related attributes on the row, from its "true"
        product record indicated by
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.product_id`.

        This is called automatically from :meth:`refresh_row()`.

        There is no default logic here; subclass must implement as
        needed.
        """

    def remove_row(self, row):
        """
        Remove a row from its batch.

        This also will update the batch
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatch.total_price`
        accordingly.
        """
        if row.total_price:
            batch = row.batch
            batch.total_price = (batch.total_price or 0) - row.total_price

        super().remove_row(row)

    def do_delete(self, batch, user, **kwargs):
        """
        Delete the given batch entirely.

        If the batch has a
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatch.pending_customer`
        record, that is deleted also.
        """
        # maybe delete pending customer record, if it only exists for
        # sake of this batch
        if batch.pending_customer:
            if len(batch.pending_customer.new_order_batches) == 1:
                # TODO: check for past orders too
                session = self.app.get_session(batch)
                session.delete(batch.pending_customer)

        # continue with normal deletion
        super().do_delete(batch, user, **kwargs)

    def why_not_execute(self, batch, **kwargs):
        """
        By default this checks to ensure the batch has a customer and
        at least one item.
        """
        if not batch.customer_id and not batch.pending_customer:
            return "Must assign the customer"

        rows = self.get_effective_rows(batch)
        if not rows:
            return "Must add at least one valid item"

    def get_effective_rows(self, batch):
        """
        Only rows with
        :attr:`~sideshow.db.model.batch.neworder.NewOrderBatchRow.STATUS_OK`
        are "effective" - i.e. rows with other status codes will not
        be created as proper order items.
        """
        return [row for row in batch.rows
                if row.status_code == row.STATUS_OK]

    def execute(self, batch, user=None, progress=None, **kwargs):
        """
        By default, this will call :meth:`make_new_order()` and return
        the new :class:`~sideshow.db.model.orders.Order` instance.

        Note that callers should use
        :meth:`~wuttjamaican:wuttjamaican.batch.BatchHandler.do_execute()`
        instead, which calls this method automatically.
        """
        rows = self.get_effective_rows(batch)
        order = self.make_new_order(batch, rows, user=user, progress=progress, **kwargs)
        return order

    def make_new_order(self, batch, rows, user=None, progress=None, **kwargs):
        """
        Create a new :term:`order` from the batch data.

        This is called automatically from :meth:`execute()`.

        :param batch:
           :class:`~sideshow.db.model.batch.neworder.NewOrderBatch`
           instance.

        :param rows: List of effective rows for the batch, i.e. which
           rows should be converted to :term:`order items <order
           item>`.

        :returns: :class:`~sideshow.db.model.orders.Order` instance.
        """
        model = self.app.model
        enum = self.app.enum
        session = self.app.get_session(batch)

        batch_fields = [
            'store_id',
            'customer_id',
            'pending_customer',
            'customer_name',
            'phone_number',
            'email_address',
            'total_price',
        ]

        row_fields = [
            'pending_product_uuid',
            'product_scancode',
            'product_brand',
            'product_description',
            'product_size',
            'product_weighed',
            'department_id',
            'department_name',
            'case_size',
            'order_qty',
            'order_uom',
            'unit_cost',
            'unit_price_quoted',
            'case_price_quoted',
            'unit_price_reg',
            'unit_price_sale',
            'sale_ends',
            # 'discount_percent',
            'total_price',
            'special_order',
        ]

        # make order
        kw = dict([(field, getattr(batch, field))
                   for field in batch_fields])
        kw['order_id'] = batch.id
        kw['created_by'] = user
        order = model.Order(**kw)
        session.add(order)
        session.flush()

        def convert(row, i):

            # make order item
            kw = dict([(field, getattr(row, field))
                       for field in row_fields])
            item = model.OrderItem(**kw)
            order.items.append(item)

            # set item status
            item.status_code = enum.ORDER_ITEM_STATUS_INITIATED

        self.app.progress_loop(convert, rows, progress,
                               message="Converting batch rows to order items")
        session.flush()
        return order
