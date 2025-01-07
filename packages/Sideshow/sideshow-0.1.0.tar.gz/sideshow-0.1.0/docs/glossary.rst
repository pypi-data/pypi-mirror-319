
Glossary
========

.. glossary::
   :sorted:

   order
     This is the central focus of the app; it refers to a customer
     case/special order which is tracked over time, from placement to
     fulfillment.  Each order may have one or more :term:`order items
     <order item>`.

   order item
     This is effectively a "line item" within an :term:`order`.  It
     represents a particular product, with quantity and pricing
     specific to the order.

     Each order item is tracked independently of its parent order and
     sibling items.

   pending customer
     Generally refers to a "new / unknown" customer, e.g. for whom a
     new order is being created.  This allows the order lifecycle to
     get going before the customer has a proper account in the system.

     See :class:`~sideshow.db.model.customers.PendingCustomer` for the
     data model.

   pending product
     Generally refers to a "new / unknown" product, e.g. for which a
     new order is being created.  This allows the order lifecycle to
     get going before the product has a true record in the system.

     See :class:`~sideshow.db.model.products.PendingProduct` for the
     data model.
