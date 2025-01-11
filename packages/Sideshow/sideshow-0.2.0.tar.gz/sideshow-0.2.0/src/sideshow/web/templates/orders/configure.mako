## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <h3 class="block is-size-3">Products</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="If set, user can enter details of an arbitrary new &quot;pending&quot; product.">
      <b-checkbox name="sideshow.orders.allow_unknown_products"
                  v-model="simpleSettings['sideshow.orders.allow_unknown_products']"
                  native-value="true"
                  @input="settingsNeedSaved = true">
        Allow creating orders for "unknown" products
      </b-checkbox>
    </b-field>

    <div v-show="simpleSettings['sideshow.orders.allow_unknown_products']"
         style="padding-left: 2rem;">

      <p class="block">
        Require these fields for new product:
      </p>

      <div class="block"
           style="margin-left: 2rem;">
        % for field in pending_product_fields:
            <b-field>
              <b-checkbox name="sideshow.orders.unknown_product.fields.${field}.required"
                          v-model="simpleSettings['sideshow.orders.unknown_product.fields.${field}.required']"
                          native-value="true"
                          @input="settingsNeedSaved = true">
                ${field}
              </b-checkbox>
            </b-field>
        % endfor
      </div>

    </div>
  </div>
</%def>
