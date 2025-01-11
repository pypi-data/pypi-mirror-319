# Order

Order information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 
**seller_order_id** | **str** | A seller-defined order identifier. | [optional] 
**purchase_date** | **str** | The date when the order was created. | 
**last_update_date** | **str** | The date when the order was last updated.  __Note__: &#x60;LastUpdateDate&#x60; is returned with an incorrect date for orders that were last updated before 2009-04-01. | 
**order_status** | **str** | The current order status. | 
**fulfillment_channel** | **str** | Whether the order was fulfilled by Amazon (&#x60;AFN&#x60;) or by the seller (&#x60;MFN&#x60;). | [optional] 
**sales_channel** | **str** | The sales channel for the first item in the order. | [optional] 
**order_channel** | **str** | The order channel for the first item in the order. | [optional] 
**ship_service_level** | **str** | The order&#39;s shipment service level. | [optional] 
**order_total** | [**Money**](Money.md) |  | [optional] 
**number_of_items_shipped** | **int** | The number of items shipped. | [optional] 
**number_of_items_unshipped** | **int** | The number of items unshipped. | [optional] 
**payment_execution_detail** | [**List[PaymentExecutionDetailItem]**](PaymentExecutionDetailItem.md) | A list of payment execution detail items. | [optional] 
**payment_method** | **str** | The payment method for the order. This property is limited to COD and CVS payment methods. Unless you need the specific COD payment information provided by the &#x60;PaymentExecutionDetailItem&#x60; object, we recommend using the &#x60;PaymentMethodDetails&#x60; property to get payment method information. | [optional] 
**payment_method_details** | **List[str]** | A list of payment method detail items. | [optional] 
**marketplace_id** | **str** | The identifier for the marketplace where the order was placed. | [optional] 
**shipment_service_level_category** | **str** | The shipment service level category for the order.  **Possible values**: &#x60;Expedited&#x60;, &#x60;FreeEconomy&#x60;, &#x60;NextDay&#x60;, &#x60;Priority&#x60;, &#x60;SameDay&#x60;, &#x60;SecondDay&#x60;, &#x60;Scheduled&#x60;, and &#x60;Standard&#x60;. | [optional] 
**easy_ship_shipment_status** | [**EasyShipShipmentStatus**](EasyShipShipmentStatus.md) |  | [optional] 
**cba_displayable_shipping_label** | **str** | Custom ship label for Checkout by Amazon (CBA). | [optional] 
**order_type** | **str** | The order&#39;s type. | [optional] 
**earliest_ship_date** | **str** | The start of the time period within which you have committed to ship the order. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. Only returned for seller-fulfilled orders.  __Note__: &#x60;EarliestShipDate&#x60; might not be returned for orders placed before February 1, 2013. | [optional] 
**latest_ship_date** | **str** | The end of the time period within which you have committed to ship the order. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. Only returned for seller-fulfilled orders.  __Note__: &#x60;LatestShipDate&#x60; might not be returned for orders placed before February 1, 2013. | [optional] 
**earliest_delivery_date** | **str** | The start of the time period within which you have committed to fulfill the order. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. Only returned for seller-fulfilled orders. | [optional] 
**latest_delivery_date** | **str** | The end of the time period within which you have committed to fulfill the order. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. Only returned for seller-fulfilled orders that do not have a &#x60;PendingAvailability&#x60;, &#x60;Pending&#x60;, or &#x60;Canceled&#x60; status. | [optional] 
**is_business_order** | **bool** | When true, the order is an Amazon Business order. An Amazon Business order is an order where the buyer is a Verified Business Buyer. | [optional] 
**is_prime** | **bool** | When true, the order is a seller-fulfilled Amazon Prime order. | [optional] 
**is_premium_order** | **bool** | When true, the order has a Premium Shipping Service Level Agreement. For more information about Premium Shipping orders, refer to \&quot;Premium Shipping Options\&quot; in the Seller Central Help for your marketplace. | [optional] 
**is_global_express_enabled** | **bool** | When true, the order is a &#x60;GlobalExpress&#x60; order. | [optional] 
**replaced_order_id** | **str** | The order ID value for the order that is being replaced. Returned only if IsReplacementOrder &#x3D; true. | [optional] 
**is_replacement_order** | **bool** | When true, this is a replacement order. | [optional] 
**promise_response_due_date** | **str** | Indicates the date by which the seller must respond to the buyer with an estimated ship date. Only returned for Sourcing on Demand orders. | [optional] 
**is_estimated_ship_date_set** | **bool** | When true, the estimated ship date is set for the order. Only returned for Sourcing on Demand orders. | [optional] 
**is_sold_by_ab** | **bool** | When true, the item within this order was bought and re-sold by Amazon Business EU SARL (ABEU). By buying and instantly re-selling your items, ABEU becomes the seller of record, making your inventory available for sale to customers who would not otherwise purchase from a third-party seller. | [optional] 
**is_iba** | **bool** | When true, the item within this order was bought and re-sold by Amazon Business EU SARL (ABEU). By buying and instantly re-selling your items, ABEU becomes the seller of record, making your inventory available for sale to customers who would not otherwise purchase from a third-party seller. | [optional] 
**default_ship_from_location_address** | [**Address**](Address.md) |  | [optional] 
**buyer_invoice_preference** | **str** | The buyer&#39;s invoicing preference. Sellers can use this data to issue electronic invoices for orders in Turkey.  **Note**: This attribute is only available in the Turkey marketplace. | [optional] 
**buyer_tax_information** | [**BuyerTaxInformation**](BuyerTaxInformation.md) |  | [optional] 
**fulfillment_instruction** | [**FulfillmentInstruction**](FulfillmentInstruction.md) |  | [optional] 
**is_ispu** | **bool** | When true, this order is marked to be picked up from a store rather than delivered. | [optional] 
**is_access_point_order** | **bool** | When true, this order is marked to be delivered to an Access Point. The access location is chosen by the customer. Access Points include Amazon Hub Lockers, Amazon Hub Counters, and pickup points operated by carriers. | [optional] 
**marketplace_tax_info** | [**MarketplaceTaxInfo**](MarketplaceTaxInfo.md) |  | [optional] 
**seller_display_name** | **str** | The seller’s friendly name registered in the marketplace where the sale took place. Sellers can use this data to issue electronic invoices for orders in Brazil.  **Note**: This attribute is only available in the Brazil marketplace for the orders with &#x60;Pending&#x60; or &#x60;Unshipped&#x60; status. | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**buyer_info** | [**BuyerInfo**](BuyerInfo.md) |  | [optional] 
**automated_shipping_settings** | [**AutomatedShippingSettings**](AutomatedShippingSettings.md) |  | [optional] 
**has_regulated_items** | **bool** | Whether the order contains regulated items which may require additional approval steps before being fulfilled. | [optional] 
**electronic_invoice_status** | [**ElectronicInvoiceStatus**](ElectronicInvoiceStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.order import Order

# TODO update the JSON string below
json = "{}"
# create an instance of Order from a JSON string
order_instance = Order.from_json(json)
# print the JSON string representation of the object
print(Order.to_json())

# convert the object into a dict
order_dict = order_instance.to_dict()
# create an instance of Order from a dict
order_from_dict = Order.from_dict(order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


