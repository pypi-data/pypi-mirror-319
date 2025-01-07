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
Sideshow Menu
"""

from wuttaweb import menus as base


class SideshowMenuHandler(base.MenuHandler):
    """
    Sideshow menu handler
    """

    def make_menus(self, request, **kwargs):
        """ """
        return [
            self.make_orders_menu(request),
            self.make_pending_menu(request),
            self.make_batch_menu(request),
            self.make_admin_menu(request),
        ]

    def make_orders_menu(self, request, **kwargs):
        """
        Generate a typical Orders menu.
        """
        return {
            'title': "Orders",
            'type': 'menu',
            'items': [
                {
                    'title': "Create New Order",
                    'route': 'orders.create',
                    'perm': 'orders.create',
                },
                {'type': 'sep'},
                {
                    'title': "All Orders",
                    'route': 'orders',
                    'perm': 'orders.list',
                },
                {
                    'title': "All Order Items",
                    'route': 'order_items',
                    'perm': 'order_items.list',
                },
            ],
        }

    def make_pending_menu(self, request, **kwargs):
        """
        Generate a typical Pending menu.
        """
        return {
            'title': "Pending",
            'type': 'menu',
            'items': [
                {
                    'title': "Customers",
                    'route': 'pending_customers',
                    'perm': 'pending_customers.list',
                },
                {
                    'title': "Products",
                    'route': 'pending_products',
                    'perm': 'pending_products.list',
                },
            ],
        }

    def make_batch_menu(self, request, **kwargs):
        """
        Generate a typical Batch menu.
        """
        return {
            'title': "Batches",
            'type': 'menu',
            'items': [
                {
                    'title': "New Orders",
                    'route': 'neworder_batches',
                    'perm': 'neworder_batches.list',
                },
            ],
        }

    def make_admin_menu(self, request, **kwargs):
        """ """
        kwargs['include_people'] = True
        return super().make_admin_menu(request, **kwargs)
