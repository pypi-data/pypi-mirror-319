# -*- coding: utf-8; -*-

import datetime
import decimal
from unittest.mock import patch

from sqlalchemy import orm
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.response import Response

from wuttaweb.forms.schema import WuttaMoney

from sideshow.batch.neworder import NewOrderBatchHandler
from sideshow.testing import WebTestCase
from sideshow.web.views import orders as mod
from sideshow.web.forms.schema import OrderRef


class TestIncludeme(WebTestCase):

    def test_coverage(self):
        mod.includeme(self.pyramid_config)


class TestOrderView(WebTestCase):

    def make_view(self):
        return mod.OrderView(self.request)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.PendingProduct)
        self.assertNotIn('order_id', grid.linked_columns)
        self.assertNotIn('total_price', grid.renderers)
        view.configure_grid(grid)
        self.assertIn('order_id', grid.linked_columns)
        self.assertIn('total_price', grid.renderers)

    def test_create(self):
        self.pyramid_config.include('sideshow.web.views')
        model = self.app.model
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.flush()

        with patch.object(view, 'Session', return_value=self.session):
            with patch.object(self.request, 'current_route_url', return_value='/orders/new'):

                # this will require some perms
                with patch.multiple(self.request, create=True,
                                    user=user, is_root=True):

                    # fetch page to start things off
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 0)
                    response = view.create()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    batch1 = self.session.query(model.NewOrderBatch).one()

                    # start over; deletes current batch
                    with patch.multiple(self.request, create=True,
                                        method='POST',
                                        POST={'action': 'start_over'}):
                        response = view.create()
                        self.assertIsInstance(response, HTTPFound)
                        self.assertIn('/orders/new', response.location)
                        self.assertEqual(self.session.query(model.NewOrderBatch).count(), 0)

                    # fetch again to get new batch
                    response = view.create()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    batch2 = self.session.query(model.NewOrderBatch).one()
                    self.assertIsNot(batch2, batch1)

                    # set pending customer
                    with patch.multiple(self.request, create=True,
                                        method='POST',
                                        json_body={'action': 'set_pending_customer',
                                                   'first_name': 'Fred',
                                                   'last_name': 'Flintstone',
                                                   'phone_number': '555-1234',
                                                   'email_address': 'fred@mailinator.com'}):
                        response = view.create()
                        self.assertIsInstance(response, Response)
                        self.assertEqual(response.content_type, 'application/json')
                        self.assertEqual(response.json_body, {
                            'customer_is_known': False,
                            'customer_id': None,
                            'customer_name': 'Fred Flintstone',
                            'phone_number': '555-1234',
                            'email_address': 'fred@mailinator.com',
                            'new_customer_name': 'Fred Flintstone',
                            'new_customer_first_name': 'Fred',
                            'new_customer_last_name': 'Flintstone',
                            'new_customer_phone': '555-1234',
                            'new_customer_email': 'fred@mailinator.com',
                        })

                    # invalid action
                    with patch.multiple(self.request, create=True,
                                        method='POST',
                                        POST={'action': 'bogus'},
                                        json_body={'action': 'bogus'}):
                        response = view.create()
                        self.assertIsInstance(response, Response)
                        self.assertEqual(response.content_type, 'application/json')
                        self.assertEqual(response.json_body, {'error': 'unknown form action'})

    def test_get_current_batch(self):
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        # user is required
        self.assertRaises(HTTPForbidden, view.get_current_batch)

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):

                    # batch is auto-created
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 0)
                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    self.assertIs(batch.created_by, user)

                    # same batch is returned subsequently
                    batch2 = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    self.assertIs(batch2, batch)

    def test_get_pending_product_required_fields(self):
        model = self.app.model
        view = self.make_view()

        # only description is required by default
        fields = view.get_pending_product_required_fields()
        self.assertEqual(fields, ['description'])

        # but config can specify otherwise
        self.config.setdefault('sideshow.orders.unknown_product.fields.brand_name.required', 'true')
        self.config.setdefault('sideshow.orders.unknown_product.fields.description.required', 'false')
        self.config.setdefault('sideshow.orders.unknown_product.fields.size.required', 'true')
        self.config.setdefault('sideshow.orders.unknown_product.fields.unit_price_reg.required', 'true')
        fields = view.get_pending_product_required_fields()
        self.assertEqual(fields, ['brand_name', 'size', 'unit_price_reg'])

    def test_get_context_customer(self):
        self.pyramid_config.add_route('orders', '/orders/')
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)

        # with true customer
        batch = handler.make_batch(self.session, created_by=user,
                                   customer_id=42, customer_name='Fred Flintstone',
                                   phone_number='555-1234', email_address='fred@mailinator.com')
        self.session.add(batch)
        self.session.flush()
        context = view.get_context_customer(batch)
        self.assertEqual(context, {
            'customer_is_known': True,
            'customer_id': 42,
            'customer_name': 'Fred Flintstone',
            'phone_number': '555-1234',
            'email_address': 'fred@mailinator.com',
            'new_customer_name': None,
            'new_customer_first_name': None,
            'new_customer_last_name': None,
            'new_customer_phone': None,
            'new_customer_email': None,
        })

        # with pending customer
        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        handler.set_pending_customer(batch, dict(
            full_name="Fred Flintstone",
            first_name="Fred", last_name="Flintstone",
            phone_number='555-1234', email_address='fred@mailinator.com',
            created_by=user,
        ))
        self.session.flush()
        context = view.get_context_customer(batch)
        self.assertEqual(context, {
            'customer_is_known': False,
            'customer_id': None,
            'customer_name': 'Fred Flintstone',
            'phone_number': '555-1234',
            'email_address': 'fred@mailinator.com',
            'new_customer_name': 'Fred Flintstone',
            'new_customer_first_name': 'Fred',
            'new_customer_last_name': 'Flintstone',
            'new_customer_phone': '555-1234',
            'new_customer_email': 'fred@mailinator.com',
        })

        # with no customer
        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.session.flush()
        context = view.get_context_customer(batch)
        self.assertEqual(context, {
            'customer_is_known': True, # nb. this is for UI default
            'customer_id': None,
            'customer_name': None,
            'phone_number': None,
            'email_address': None,
            'new_customer_name': None,
            'new_customer_first_name': None,
            'new_customer_last_name': None,
            'new_customer_phone': None,
            'new_customer_email': None,
        })

    def test_start_over(self):
        self.pyramid_config.add_route('orders.create', '/orders/new')
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):

                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    result = view.start_over(batch)
                    self.assertIsInstance(result, HTTPFound)
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 0)

    def test_cancel_order(self):
        self.pyramid_config.add_route('orders', '/orders/')
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):

                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 1)
                    result = view.cancel_order(batch)
                    self.assertIsInstance(result, HTTPFound)
                    self.session.flush()
                    self.assertEqual(self.session.query(model.NewOrderBatch).count(), 0)

    def test_set_pending_customer(self):
        self.pyramid_config.add_route('orders.create', '/orders/new')
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        data = {
            'first_name': 'Fred',
            'last_name': 'Flintstone',
            'phone_number': '555-1234',
            'email_address': 'fred@mailinator.com',
        }

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):
                    batch = view.get_current_batch()
                    self.session.flush()

                    # normal
                    self.assertIsNone(batch.pending_customer)
                    context = view.set_pending_customer(batch, data)
                    self.assertIsInstance(batch.pending_customer, model.PendingCustomer)
                    self.assertEqual(context, {
                        'customer_is_known': False,
                        'customer_id': None,
                        'customer_name': 'Fred Flintstone',
                        'phone_number': '555-1234',
                        'email_address': 'fred@mailinator.com',
                        'new_customer_name': 'Fred Flintstone',
                        'new_customer_first_name': 'Fred',
                        'new_customer_last_name': 'Flintstone',
                        'new_customer_phone': '555-1234',
                        'new_customer_email': 'fred@mailinator.com',
                    })

                    # error
                    with patch.object(handler, 'set_pending_customer', side_effect=RuntimeError):
                        context = view.set_pending_customer(batch, data)
                        self.assertEqual(context, {
                            'error': 'RuntimeError',
                        })

    def test_add_item(self):
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        data = {
            'pending_product': {
                'scancode': '07430500132',
                'brand_name': 'Bragg',
                'description': 'Vinegar',
                'size': '32oz',
                'unit_price_reg': 5.99,
            },
            'order_qty': 1,
            'order_uom': enum.ORDER_UOM_UNIT,
        }

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):
                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(len(batch.rows), 0)

                    # normal pending product
                    result = view.add_item(batch, data)
                    self.assertIn('batch', result)
                    self.assertIn('row', result)
                    self.session.flush()
                    self.assertEqual(len(batch.rows), 1)
                    row = batch.rows[0]
                    self.assertIsInstance(row.pending_product, model.PendingProduct)

                    # pending w/ invalid price
                    with patch.dict(data['pending_product'], unit_price_reg='invalid'):
                        result = view.add_item(batch, data)
                        self.assertEqual(result, {'error': "Invalid entry for field: unit_price_reg"})
                        self.session.flush()
                        self.assertEqual(len(batch.rows), 1) # still just the 1st row

                    # true product not yet supported
                    with patch.dict(data, product_is_known=True):
                        self.assertRaises(NotImplementedError, view.add_item, batch, data)

    def test_update_item(self):
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        data = {
            'pending_product': {
                'scancode': '07430500132',
                'brand_name': 'Bragg',
                'description': 'Vinegar',
                'size': '32oz',
                'unit_price_reg': 5.99,
                'case_size': 12,
            },
            'order_qty': 1,
            'order_uom': enum.ORDER_UOM_CASE,
        }

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):
                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(len(batch.rows), 0)

                    # add row w/ pending product
                    view.add_item(batch, data)
                    self.session.flush()
                    row = batch.rows[0]
                    self.assertIsInstance(row.pending_product, model.PendingProduct)
                    self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))

                    # missing row uuid
                    result = view.update_item(batch, data)
                    self.assertEqual(result, {'error': "Must specify a row UUID"})

                    # row not found
                    with patch.dict(data, uuid=self.app.make_true_uuid()):
                        result = view.update_item(batch, data)
                        self.assertEqual(result, {'error': "Row not found"})

                    # row for wrong batch
                    batch2 = handler.make_batch(self.session, created_by=user)
                    self.session.add(batch2)
                    row2 = handler.make_row(order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
                    handler.add_row(batch2, row2)
                    self.session.flush()
                    with patch.dict(data, uuid=row2.uuid):
                        result = view.update_item(batch, data)
                        self.assertEqual(result, {'error': "Row is for wrong batch"})

                    # set row for remaining tests
                    data['uuid'] = row.uuid

                    # true product not yet supported
                    with patch.dict(data, product_is_known=True):
                        self.assertRaises(NotImplementedError, view.update_item, batch, data)

                    # update row, pending product
                    with patch.dict(data, order_qty=2):
                        with patch.dict(data['pending_product'], scancode='07430500116'):
                            self.assertEqual(row.product_scancode, '07430500132')
                            self.assertEqual(row.order_qty, 1)
                            result = view.update_item(batch, data)
                            self.assertEqual(sorted(result), ['batch', 'row'])
                            self.assertEqual(row.product_scancode, '07430500116')
                            self.assertEqual(row.order_qty, 2)
                            self.assertEqual(row.pending_product.scancode, '07430500116')
                            self.assertEqual(result['row']['product_scancode'], '07430500116')
                            self.assertEqual(result['row']['order_qty'], '2')

    def test_delete_item(self):
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        data = {
            'pending_product': {
                'scancode': '07430500132',
                'brand_name': 'Bragg',
                'description': 'Vinegar',
                'size': '32oz',
                'unit_price_reg': 5.99,
                'case_size': 12,
            },
            'order_qty': 1,
            'order_uom': enum.ORDER_UOM_CASE,
        }

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):
                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(len(batch.rows), 0)

                    # add row w/ pending product
                    view.add_item(batch, data)
                    self.session.flush()
                    row = batch.rows[0]
                    self.assertIsInstance(row.pending_product, model.PendingProduct)
                    self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))

                    # missing row uuid
                    result = view.delete_item(batch, data)
                    self.assertEqual(result, {'error': "Must specify a row UUID"})

                    # row not found
                    with patch.dict(data, uuid=self.app.make_true_uuid()):
                        result = view.delete_item(batch, data)
                        self.assertEqual(result, {'error': "Row not found"})

                    # row for wrong batch
                    batch2 = handler.make_batch(self.session, created_by=user)
                    self.session.add(batch2)
                    row2 = handler.make_row(order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
                    handler.add_row(batch2, row2)
                    self.session.flush()
                    with patch.dict(data, uuid=row2.uuid):
                        result = view.delete_item(batch, data)
                        self.assertEqual(result, {'error': "Row is for wrong batch"})

                    # row is deleted
                    data['uuid'] = row.uuid
                    self.assertEqual(len(batch.rows), 1)
                    self.assertEqual(batch.row_count, 1)
                    result = view.delete_item(batch, data)
                    self.assertEqual(sorted(result), ['batch'])
                    self.session.refresh(batch)
                    self.assertEqual(len(batch.rows), 0)
                    self.assertEqual(batch.row_count, 0)

    def test_submit_new_order(self):
        self.pyramid_config.add_route('orders.view', '/orders/{uuid}')
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        self.session.commit()

        data = {
            'pending_product': {
                'scancode': '07430500132',
                'brand_name': 'Bragg',
                'description': 'Vinegar',
                'size': '32oz',
                'unit_price_reg': 5.99,
                'case_size': 12,
            },
            'order_qty': 1,
            'order_uom': enum.ORDER_UOM_CASE,
        }

        with patch.object(view, 'batch_handler', create=True, new=handler):
            with patch.object(view, 'Session', return_value=self.session):
                with patch.object(self.request, 'user', new=user):
                    batch = view.get_current_batch()
                    self.session.flush()
                    self.assertEqual(len(batch.rows), 0)

                    # add row w/ pending product
                    view.add_item(batch, data)
                    self.session.flush()
                    row = batch.rows[0]
                    self.assertIsInstance(row.pending_product, model.PendingProduct)
                    self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))

                    # execute not allowed yet (no customer)
                    result = view.submit_new_order(batch, {})
                    self.assertEqual(result, {'error': "Must assign the customer"})

                    # submit/execute ok
                    batch.customer_id = 42
                    result = view.submit_new_order(batch, {})
                    self.assertEqual(sorted(result), ['next_url'])
                    self.assertIn('/orders/', result['next_url'])

                    # error (already executed)
                    result = view.submit_new_order(batch, {})
                    self.assertEqual(result, {
                        'error': f"ValueError: batch has already been executed: {batch}",
                    })

    def test_get_default_uom_choices(self):
        enum = self.app.enum
        view = self.make_view()

        uoms = view.get_default_uom_choices()
        self.assertEqual(uoms, [{'key': key, 'value': val}
                                for key, val in enum.ORDER_UOM.items()])

    def test_normalize_batch(self):
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        pending = {
            'scancode': '07430500132',
            'brand_name': 'Bragg',
            'description': 'Vinegar',
            'size': '32oz',
            'unit_price_reg': 5.99,
            'case_size': 12,
            'created_by': user,
        }
        row = handler.add_pending_product(batch, pending, 1, enum.ORDER_UOM_CASE)
        self.session.commit()

        data = view.normalize_batch(batch)
        self.assertEqual(data, {
            'uuid': batch.uuid.hex,
            'total_price': '71.880',
            'total_price_display': '$71.88',
            'status_code': None,
            'status_text': None,
        })

    def test_normalize_row(self):
        model = self.app.model
        enum = self.app.enum
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        pending = {
            'scancode': '07430500132',
            'brand_name': 'Bragg',
            'description': 'Vinegar',
            'size': '32oz',
            'unit_price_reg': 5.99,
            'case_size': 12,
            'created_by': user,
        }
        row = handler.add_pending_product(batch, pending, 2, enum.ORDER_UOM_CASE)
        self.session.commit()

        # normal
        data = view.normalize_row(row)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['uuid'], row.uuid.hex)
        self.assertEqual(data['sequence'], 1)
        self.assertEqual(data['product_scancode'], '07430500132')
        self.assertEqual(data['case_size'], '12')
        self.assertEqual(data['order_qty'], '2')
        self.assertEqual(data['order_uom'], 'CS')
        self.assertEqual(data['order_qty_display'], '2 Cases (&times; 12 = 24 Units)')
        self.assertEqual(data['unit_price_reg'], 5.99)
        self.assertEqual(data['unit_price_reg_display'], '$5.99')
        self.assertNotIn('unit_price_sale', data)
        self.assertNotIn('unit_price_sale_display', data)
        self.assertNotIn('sale_ends', data)
        self.assertNotIn('sale_ends_display', data)
        self.assertEqual(data['unit_price_quoted'], 5.99)
        self.assertEqual(data['unit_price_quoted_display'], '$5.99')
        self.assertEqual(data['case_price_quoted'], 71.88)
        self.assertEqual(data['case_price_quoted_display'], '$71.88')
        self.assertEqual(data['total_price'], 143.76)
        self.assertEqual(data['total_price_display'], '$143.76')
        self.assertIsNone(data['special_order'])
        self.assertEqual(data['status_code'], row.STATUS_OK)
        self.assertEqual(data['pending_product'], {
            'uuid': row.pending_product_uuid.hex,
            'scancode': '07430500132',
            'brand_name': 'Bragg',
            'description': 'Vinegar',
            'size': '32oz',
            'department_id': None,
            'department_name': None,
            'unit_price_reg': 5.99,
            'vendor_name': None,
            'vendor_item_code': None,
            'unit_cost': None,
            'case_size': 12.0,
            'notes': None,
            'special_order': None,
        })

        # unknown case size
        row.pending_product.case_size = None
        handler.refresh_row(row)
        self.session.flush()
        data = view.normalize_row(row)
        self.assertEqual(data['order_qty_display'], '2 Cases (&times; ?? = ?? Units)')

        # order by unit
        row.order_uom = enum.ORDER_UOM_UNIT
        handler.refresh_row(row)
        self.session.flush()
        data = view.normalize_row(row)
        self.assertEqual(data['order_qty_display'], '2 Units')

        # item on sale
        row.pending_product.case_size = 12
        row.unit_price_sale = decimal.Decimal('5.19')
        row.sale_ends = datetime.datetime(2025, 1, 5, 20, 32)
        handler.refresh_row(row, now=datetime.datetime(2025, 1, 5, 19))
        self.session.flush()
        data = view.normalize_row(row)
        self.assertEqual(data['unit_price_sale'], 5.19)
        self.assertEqual(data['unit_price_sale_display'], '$5.19')
        self.assertEqual(data['sale_ends'], '2025-01-05 20:32:00')
        self.assertEqual(data['sale_ends_display'], '2025-01-05')
        self.assertEqual(data['unit_price_quoted'], 5.19)
        self.assertEqual(data['unit_price_quoted_display'], '$5.19')
        self.assertEqual(data['case_price_quoted'], 62.28)
        self.assertEqual(data['case_price_quoted_display'], '$62.28')

    def test_get_instance_title(self):
        model = self.app.model
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, customer_name="Fred Flintstone", created_by=user)
        self.session.add(order)
        self.session.flush()

        title = view.get_instance_title(order)
        self.assertEqual(title, "#42 for Fred Flintstone")

    def test_configure_form(self):
        model = self.app.model
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        self.session.commit()

        # viewing
        with patch.object(view, 'viewing', new=True):
            form = view.make_form(model_instance=order)
            # nb. this is to avoid include/exclude ambiguity
            form.remove('items')
            view.configure_form(form)
            schema = form.get_schema()
            self.assertIsInstance(schema['total_price'].typ, WuttaMoney)

    def test_get_xref_buttons(self):
        self.pyramid_config.add_route('neworder_batches.view', '/batch/neworder/{uuid}')
        model = self.app.model
        handler = NewOrderBatchHandler(self.config)
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        self.session.flush()

        with patch.object(view, 'Session', return_value=self.session):

            # nb. this requires perm to view batch
            with patch.object(self.request, 'is_root', new=True):

                # order has no batch, so no buttons
                buttons = view.get_xref_buttons(order)
                self.assertEqual(buttons, [])

                # mock up a batch to get a button
                batch = handler.make_batch(self.session,
                                           id=order.order_id,
                                           created_by=user,
                                           executed=datetime.datetime.now(),
                                           executed_by=user)
                self.session.add(batch)
                self.session.flush()
                buttons = view.get_xref_buttons(order)
                self.assertEqual(len(buttons), 1)
                button = buttons[0]
                self.assertIn("View the Batch", button)

    def test_get_row_grid_data(self):
        model = self.app.model
        enum = self.app.enum
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        self.session.flush()
        order.items.append(model.OrderItem(product_id='07430500132',
                                           product_scancode='07430500132',
                                           order_qty=1, order_uom=enum.ORDER_UOM_UNIT,
                                           status_code=enum.ORDER_ITEM_STATUS_INITIATED))
        self.session.flush()

        with patch.object(view, 'Session', return_value=self.session):
            query = view.get_row_grid_data(order)
            self.assertIsInstance(query, orm.Query)
            items = query.all()
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].product_scancode, '07430500132')

    def test_configure_row_grid(self):
        model = self.app.model
        enum = self.app.enum
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        self.session.flush()
        order.items.append(model.OrderItem(product_id='07430500132',
                                           product_scancode='07430500132',
                                           order_qty=1, order_uom=enum.ORDER_UOM_UNIT,
                                           status_code=enum.ORDER_ITEM_STATUS_INITIATED))
        self.session.flush()

        with patch.object(view, 'Session', return_value=self.session):
            grid = view.make_grid(model_class=model.OrderItem, data=order.items)
            self.assertNotIn('product_scancode', grid.linked_columns)
            view.configure_row_grid(grid)
            self.assertIn('product_scancode', grid.linked_columns)

    def test_render_status_code(self):
        enum = self.app.enum
        view = self.make_view()
        result = view.render_status_code(None, None, enum.ORDER_ITEM_STATUS_INITIATED)
        self.assertEqual(result, "initiated")
        self.assertEqual(result, enum.ORDER_ITEM_STATUS[enum.ORDER_ITEM_STATUS_INITIATED])

    def test_get_row_action_url_view(self):
        self.pyramid_config.add_route('order_items.view', '/order-items/{uuid}')
        model = self.app.model
        enum = self.app.enum
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        self.session.flush()
        item = model.OrderItem(product_id='07430500132',
                               product_scancode='07430500132',
                               order_qty=1, order_uom=enum.ORDER_UOM_UNIT,
                               status_code=enum.ORDER_ITEM_STATUS_INITIATED)
        order.items.append(item)
        self.session.flush()

        url = view.get_row_action_url_view(item, 0)
        self.assertIn(f'/order-items/{item.uuid}', url)


class TestOrderItemView(WebTestCase):

    def make_view(self):
        return mod.OrderItemView(self.request)

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.OrderItem)
        self.assertNotIn('order_id', grid.linked_columns)
        view.configure_grid(grid)
        self.assertIn('order_id', grid.linked_columns)

    def test_render_order_id(self):
        model = self.app.model
        view = self.make_view()
        order = model.Order(order_id=42)
        item = model.OrderItem()
        order.items.append(item)
        self.assertEqual(view.render_order_id(item, None, None), 42)

    def test_render_status_code(self):
        enum = self.app.enum
        view = self.make_view()
        self.assertEqual(view.render_status_code(None, None, enum.ORDER_ITEM_STATUS_INITIATED),
                         'initiated')

    def test_configure_form(self):
        model = self.app.model
        enum = self.app.enum
        view = self.make_view()

        item = model.OrderItem(status_code=enum.ORDER_ITEM_STATUS_INITIATED)

        # viewing
        with patch.object(view, 'viewing', new=True):
            form = view.make_form(model_instance=item)
            view.configure_form(form)
            schema = form.get_schema()
            self.assertIsInstance(schema['order'].typ, OrderRef)

    def test_get_xref_buttons(self):
        self.pyramid_config.add_route('orders.view', '/orders/{uuid}')
        model = self.app.model
        enum = self.app.enum
        view = self.make_view()

        user = model.User(username='barney')
        self.session.add(user)
        order = model.Order(order_id=42, created_by=user)
        self.session.add(order)
        item = model.OrderItem(order_qty=1, order_uom=enum.ORDER_UOM_UNIT,
                               status_code=enum.ORDER_ITEM_STATUS_INITIATED)
        order.items.append(item)
        self.session.flush()

        # nb. this requires perms
        with patch.object(self.request, 'is_root', new=True):

            # one button by default
            buttons = view.get_xref_buttons(item)
            self.assertEqual(len(buttons), 1)
            self.assertIn("View the Order", buttons[0])
