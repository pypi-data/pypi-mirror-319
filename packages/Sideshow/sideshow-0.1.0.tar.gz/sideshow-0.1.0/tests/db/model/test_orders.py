# -*- coding: utf-8; -*-

from wuttjamaican.testing import DataTestCase

from sideshow.db.model import orders as mod
from sideshow.db.model.products import PendingProduct


class TestOrder(DataTestCase):

    def test_str(self):

        order = mod.Order()
        self.assertEqual(str(order), "None")

        order = mod.Order(order_id=42)
        self.assertEqual(str(order), "42")


class TestOrderItem(DataTestCase):

    def test_str(self):

        item = mod.OrderItem()
        self.assertEqual(str(item), "")

        item = mod.OrderItem(product_description="Vinegar")
        self.assertEqual(str(item), "Vinegar")

        product = PendingProduct(brand_name="Bragg",
                                 description="Vinegar",
                                 size="32oz")
        item = mod.OrderItem(pending_product=product)
        self.assertEqual(str(item), "Bragg Vinegar 32oz")
