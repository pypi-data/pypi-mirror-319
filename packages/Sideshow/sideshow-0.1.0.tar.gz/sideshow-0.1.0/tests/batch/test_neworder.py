# -*- coding: utf-8; -*-

import decimal

from wuttjamaican.testing import DataTestCase

from sideshow.batch import neworder as mod


class TestNewOrderBatchHandler(DataTestCase):

    def make_config(self, **kwargs):
        config = super().make_config(**kwargs)
        config.setdefault('wutta.model_spec', 'sideshow.db.model')
        config.setdefault('wutta.enum_spec', 'sideshow.enum')
        return config

    def make_handler(self):
        return mod.NewOrderBatchHandler(self.config)

    def test_set_pending_customer(self):
        model = self.app.model
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user, customer_id=42)
        self.assertEqual(batch.customer_id, 42)
        self.assertIsNone(batch.pending_customer)
        self.assertIsNone(batch.customer_name)
        self.assertIsNone(batch.phone_number)
        self.assertIsNone(batch.email_address)

        # auto full_name
        handler.set_pending_customer(batch, {
            'first_name': "Fred",
            'last_name': "Flintstone",
            'phone_number': '555-1234',
            'email_address': 'fred@mailinator.com',
        })
        self.assertIsNone(batch.customer_id)
        self.assertIsInstance(batch.pending_customer, model.PendingCustomer)
        customer = batch.pending_customer
        self.assertEqual(customer.full_name, "Fred Flintstone")
        self.assertEqual(customer.first_name, "Fred")
        self.assertEqual(customer.last_name, "Flintstone")
        self.assertEqual(customer.phone_number, '555-1234')
        self.assertEqual(customer.email_address, 'fred@mailinator.com')
        self.assertEqual(batch.customer_name, "Fred Flintstone")
        self.assertEqual(batch.phone_number, '555-1234')
        self.assertEqual(batch.email_address, 'fred@mailinator.com')

        # explicit full_name
        batch = handler.make_batch(self.session, created_by=user, customer_id=42)
        handler.set_pending_customer(batch, {
            'full_name': "Freddy Flintstone",
            'first_name': "Fred",
            'last_name': "Flintstone",
            'phone_number': '555-1234',
            'email_address': 'fred@mailinator.com',
        })
        self.assertIsNone(batch.customer_id)
        self.assertIsInstance(batch.pending_customer, model.PendingCustomer)
        customer = batch.pending_customer
        self.assertEqual(customer.full_name, "Freddy Flintstone")
        self.assertEqual(customer.first_name, "Fred")
        self.assertEqual(customer.last_name, "Flintstone")
        self.assertEqual(customer.phone_number, '555-1234')
        self.assertEqual(customer.email_address, 'fred@mailinator.com')
        self.assertEqual(batch.customer_name, "Freddy Flintstone")
        self.assertEqual(batch.phone_number, '555-1234')
        self.assertEqual(batch.email_address, 'fred@mailinator.com')

    def test_add_pending_product(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.assertEqual(len(batch.rows), 0)

        kw = dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        )
        row = handler.add_pending_product(batch, kw, 1, enum.ORDER_UOM_UNIT)
        self.assertEqual(len(batch.rows), 1)
        self.assertIs(batch.rows[0], row)

        self.assertEqual(row.product_scancode, '07430500132')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '32oz')
        self.assertEqual(row.case_size, 12)
        self.assertEqual(row.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(row.unit_price_reg, decimal.Decimal('5.99'))
        self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))
        self.assertEqual(row.case_price_quoted, decimal.Decimal('71.88'))

        product = row.pending_product
        self.assertIsInstance(product, model.PendingProduct)
        self.assertEqual(product.scancode, '07430500132')
        self.assertEqual(product.brand_name, 'Bragg')
        self.assertEqual(product.description, 'Vinegar')
        self.assertEqual(product.size, '32oz')
        self.assertEqual(product.case_size, 12)
        self.assertEqual(product.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(product.unit_price_reg, decimal.Decimal('5.99'))
        self.assertIs(product.created_by, user)

    def test_set_pending_product(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.assertEqual(len(batch.rows), 0)

        # start with mock product_id
        row = handler.make_row(product_id=42, order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        handler.add_row(batch, row)
        self.session.flush()
        self.assertEqual(row.product_id, 42)
        self.assertIsNone(row.pending_product)
        self.assertIsNone(row.product_scancode)
        self.assertIsNone(row.product_brand)
        self.assertIsNone(row.product_description)
        self.assertIsNone(row.product_size)
        self.assertIsNone(row.case_size)
        self.assertIsNone(row.unit_cost)
        self.assertIsNone(row.unit_price_reg)
        self.assertIsNone(row.unit_price_quoted)

        # set pending, which clears product_id
        handler.set_pending_product(row, dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        ))
        self.session.flush()
        self.assertIsNone(row.product_id)
        self.assertIsInstance(row.pending_product, model.PendingProduct)
        self.assertEqual(row.product_scancode, '07430500132')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '32oz')
        self.assertEqual(row.case_size, 12)
        self.assertEqual(row.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(row.unit_price_reg, decimal.Decimal('5.99'))
        self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))
        self.assertEqual(row.case_price_quoted, decimal.Decimal('71.88'))
        product = row.pending_product
        self.assertIsInstance(product, model.PendingProduct)
        self.assertEqual(product.scancode, '07430500132')
        self.assertEqual(product.brand_name, 'Bragg')
        self.assertEqual(product.description, 'Vinegar')
        self.assertEqual(product.size, '32oz')
        self.assertEqual(product.case_size, 12)
        self.assertEqual(product.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(product.unit_price_reg, decimal.Decimal('5.99'))
        self.assertIs(product.created_by, user)

        # set again to update pending
        handler.set_pending_product(row, dict(
            scancode='07430500116',
            size='16oz',
            unit_cost=decimal.Decimal('2.19'),
            unit_price_reg=decimal.Decimal('3.59'),
        ))
        self.session.flush()
        self.assertIsNone(row.product_id)
        self.assertIsInstance(row.pending_product, model.PendingProduct)
        self.assertEqual(row.product_scancode, '07430500116')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '16oz')
        self.assertEqual(row.case_size, 12)
        self.assertEqual(row.unit_cost, decimal.Decimal('2.19'))
        self.assertEqual(row.unit_price_reg, decimal.Decimal('3.59'))
        self.assertEqual(row.unit_price_quoted, decimal.Decimal('3.59'))
        self.assertEqual(row.case_price_quoted, decimal.Decimal('43.08'))
        product = row.pending_product
        self.assertIsInstance(product, model.PendingProduct)
        self.assertEqual(product.scancode, '07430500116')
        self.assertEqual(product.brand_name, 'Bragg')
        self.assertEqual(product.description, 'Vinegar')
        self.assertEqual(product.size, '16oz')
        self.assertEqual(product.case_size, 12)
        self.assertEqual(product.unit_cost, decimal.Decimal('2.19'))
        self.assertEqual(product.unit_price_reg, decimal.Decimal('3.59'))
        self.assertIs(product.created_by, user)

    def test_refresh_row(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.assertEqual(len(batch.rows), 0)

        # missing product
        row = handler.make_row(order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        self.assertIsNone(row.status_code)
        handler.add_row(batch, row)
        self.assertEqual(row.status_code, row.STATUS_MISSING_PRODUCT)

        # missing order_qty
        row = handler.make_row(product_id=42, order_uom=enum.ORDER_UOM_UNIT)
        self.assertIsNone(row.status_code)
        handler.add_row(batch, row)
        self.assertEqual(row.status_code, row.STATUS_MISSING_ORDER_QTY)

        # refreshed from pending product (null price)
        product = model.PendingProduct(scancode='07430500132',
                                       brand_name='Bragg',
                                       description='Vinegar',
                                       size='32oz',
                                       created_by=user,
                                       status=enum.PendingProductStatus.PENDING)
        row = handler.make_row(pending_product=product, order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        self.assertIsNone(row.status_code)
        handler.add_row(batch, row)
        self.assertEqual(row.status_code, row.STATUS_OK)
        self.assertIsNone(row.product_id)
        self.assertIs(row.pending_product, product)
        self.assertEqual(row.product_scancode, '07430500132')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '32oz')
        self.assertIsNone(row.case_size)
        self.assertIsNone(row.unit_cost)
        self.assertIsNone(row.unit_price_reg)
        self.assertIsNone(row.unit_price_quoted)
        self.assertIsNone(row.case_price_quoted)
        self.assertIsNone(row.total_price)

        # refreshed from pending product (zero price)
        product = model.PendingProduct(scancode='07430500132',
                                       brand_name='Bragg',
                                       description='Vinegar',
                                       size='32oz',
                                       unit_price_reg=0,
                                       created_by=user,
                                       status=enum.PendingProductStatus.PENDING)
        row = handler.make_row(pending_product=product, order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        self.assertIsNone(row.status_code)
        handler.add_row(batch, row)
        self.assertEqual(row.status_code, row.STATUS_OK)
        self.assertIsNone(row.product_id)
        self.assertIs(row.pending_product, product)
        self.assertEqual(row.product_scancode, '07430500132')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '32oz')
        self.assertIsNone(row.case_size)
        self.assertIsNone(row.unit_cost)
        self.assertEqual(row.unit_price_reg, 0)
        self.assertEqual(row.unit_price_quoted, 0)
        self.assertIsNone(row.case_price_quoted)
        self.assertEqual(row.total_price, 0)

        # refreshed from pending product (normal, case)
        product = model.PendingProduct(scancode='07430500132',
                                       brand_name='Bragg',
                                       description='Vinegar',
                                       size='32oz',
                                       case_size=12,
                                       unit_cost=decimal.Decimal('3.99'),
                                       unit_price_reg=decimal.Decimal('5.99'),
                                       created_by=user,
                                       status=enum.PendingProductStatus.PENDING)
        row = handler.make_row(pending_product=product, order_qty=2, order_uom=enum.ORDER_UOM_CASE)
        self.assertIsNone(row.status_code)
        handler.add_row(batch, row)
        self.assertEqual(row.status_code, row.STATUS_OK)
        self.assertIsNone(row.product_id)
        self.assertIs(row.pending_product, product)
        self.assertEqual(row.product_scancode, '07430500132')
        self.assertEqual(row.product_brand, 'Bragg')
        self.assertEqual(row.product_description, 'Vinegar')
        self.assertEqual(row.product_size, '32oz')
        self.assertEqual(row.case_size, 12)
        self.assertEqual(row.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(row.unit_price_reg, decimal.Decimal('5.99'))
        self.assertEqual(row.unit_price_quoted, decimal.Decimal('5.99'))
        self.assertEqual(row.case_price_quoted, decimal.Decimal('71.88'))
        self.assertEqual(row.total_price, decimal.Decimal('143.76'))

    def test_remove_row(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.assertEqual(len(batch.rows), 0)

        kw = dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        )
        row = handler.add_pending_product(batch, kw, 1, enum.ORDER_UOM_CASE)
        self.session.add(row)
        self.session.flush()
        self.assertEqual(batch.row_count, 1)
        self.assertEqual(row.total_price, decimal.Decimal('71.88'))
        self.assertEqual(batch.total_price, decimal.Decimal('71.88'))

        handler.do_remove_row(row)
        self.assertEqual(batch.row_count, 0)
        self.assertEqual(batch.total_price, 0)

    def test_do_delete(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        # make batch w/ pending customer
        customer = model.PendingCustomer(full_name="Fred Flintstone",
                                         status=enum.PendingCustomerStatus.PENDING,
                                         created_by=user)
        self.session.add(customer)
        batch = handler.make_batch(self.session, created_by=user, pending_customer=customer)
        self.session.add(batch)
        self.session.commit()

        # deleting batch will also delete pending customer
        self.assertIn(batch, self.session)
        self.assertEqual(self.session.query(model.PendingCustomer).count(), 1)
        handler.do_delete(batch, user)
        self.session.commit()
        self.assertNotIn(batch, self.session)
        self.assertEqual(self.session.query(model.PendingCustomer).count(), 0)

        # make new pending customer
        customer = model.PendingCustomer(full_name="Fred Flintstone",
                                         status=enum.PendingCustomerStatus.PENDING,
                                         created_by=user)
        self.session.add(customer)

        # make 2 batches with same pending customer
        batch1 = handler.make_batch(self.session, created_by=user, pending_customer=customer)
        batch2 = handler.make_batch(self.session, created_by=user, pending_customer=customer)
        self.session.add(batch1)
        self.session.add(batch2)
        self.session.commit()

        # deleting 1 will not delete pending customer
        self.assertEqual(self.session.query(model.PendingCustomer).count(), 1)
        handler.do_delete(batch1, user)
        self.session.commit()
        self.assertEqual(self.session.query(model.PendingCustomer).count(), 1)
        self.assertIs(batch2.pending_customer, customer)

    def test_get_effective_rows(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        # make batch w/ different status rows
        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        # STATUS_MISSING_PRODUCT
        row = handler.make_row(order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        handler.add_row(batch, row)
        self.session.add(row)
        self.session.flush()
        # STATUS_MISSING_ORDER_QTY
        row = handler.make_row(product_id=42, order_qty=0, order_uom=enum.ORDER_UOM_UNIT)
        handler.add_row(batch, row)
        self.session.add(row)
        self.session.flush()
        # STATUS_OK
        row = handler.make_row(product_id=42, order_qty=1, order_uom=enum.ORDER_UOM_UNIT)
        handler.add_row(batch, row)
        self.session.add(row)
        self.session.commit()

        # only 1 effective row
        rows = handler.get_effective_rows(batch)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row.status_code, row.STATUS_OK)

    def test_why_not_execute(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user)
        self.session.add(batch)
        self.session.flush()

        reason = handler.why_not_execute(batch)
        self.assertEqual(reason, "Must assign the customer")

        batch.customer_id = 42

        reason = handler.why_not_execute(batch)
        self.assertEqual(reason, "Must add at least one valid item")

        kw = dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        )
        row = handler.add_pending_product(batch, kw, 1, enum.ORDER_UOM_CASE)
        self.session.add(row)
        self.session.flush()

        reason = handler.why_not_execute(batch)
        self.assertIsNone(reason)

    def test_make_new_order(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user,
                                   customer_id=42, customer_name="John Doe")
        self.session.add(batch)
        kw = dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        )
        row = handler.add_pending_product(batch, kw, 1, enum.ORDER_UOM_CASE)
        self.session.add(row)
        self.session.flush()

        order = handler.make_new_order(batch, [row], user=user)
        self.assertIsInstance(order, model.Order)
        self.assertIs(order.created_by, user)
        self.assertEqual(order.customer_id, 42)
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(len(order.items), 1)
        item = order.items[0]
        self.assertEqual(item.product_scancode, '07430500132')
        self.assertEqual(item.product_brand, 'Bragg')
        self.assertEqual(item.product_description, 'Vinegar')
        self.assertEqual(item.product_size, '32oz')
        self.assertEqual(item.case_size, 12)
        self.assertEqual(item.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(item.unit_price_reg, decimal.Decimal('5.99'))

    def test_execute(self):
        model = self.app.model
        enum = self.app.enum
        handler = self.make_handler()

        user = model.User(username='barney')
        self.session.add(user)

        batch = handler.make_batch(self.session, created_by=user,
                                   customer_id=42, customer_name="John Doe")
        self.session.add(batch)
        kw = dict(
            scancode='07430500132',
            brand_name='Bragg',
            description='Vinegar',
            size='32oz',
            case_size=12,
            unit_cost=decimal.Decimal('3.99'),
            unit_price_reg=decimal.Decimal('5.99'),
            created_by=user,
        )
        row = handler.add_pending_product(batch, kw, 1, enum.ORDER_UOM_CASE)
        self.session.add(row)
        self.session.flush()

        order = handler.execute(batch, user=user)
        self.assertIsInstance(order, model.Order)
        self.assertIs(order.created_by, user)
        self.assertEqual(order.customer_id, 42)
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(len(order.items), 1)
        item = order.items[0]
        self.assertEqual(item.product_scancode, '07430500132')
        self.assertEqual(item.product_brand, 'Bragg')
        self.assertEqual(item.product_description, 'Vinegar')
        self.assertEqual(item.product_size, '32oz')
        self.assertEqual(item.case_size, 12)
        self.assertEqual(item.unit_cost, decimal.Decimal('3.99'))
        self.assertEqual(item.unit_price_reg, decimal.Decimal('5.99'))
