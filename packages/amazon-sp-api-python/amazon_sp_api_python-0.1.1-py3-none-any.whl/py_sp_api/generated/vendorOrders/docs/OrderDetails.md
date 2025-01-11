# OrderDetails

Details of an order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_date** | **datetime** | The date the purchase order was placed. Must be in ISO-8601 date/time format. | 
**purchase_order_changed_date** | **datetime** | The date when purchase order was last changed by Amazon after the order was placed. This date will be greater than &#39;purchaseOrderDate&#39;. This means the PO data was changed on that date and vendors are required to fulfill the  updated PO. The PO changes can be related to Item Quantity, Ship to Location, Ship Window etc. This field will not be present in orders that have not changed after creation. Must be in ISO-8601 date/time format. | [optional] 
**purchase_order_state_changed_date** | **datetime** | The date when current purchase order state was changed. Current purchase order state is available in the field &#39;purchaseOrderState&#39;. Must be in ISO-8601 date/time format. | 
**purchase_order_type** | **str** | Type of purchase order. | [optional] 
**import_details** | [**ImportDetails**](ImportDetails.md) |  | [optional] 
**deal_code** | **str** | If requested by the recipient, this field will contain a promotional/deal number. The discount code line is optional. It is used to obtain a price discount on items on the order. | [optional] 
**payment_method** | **str** | Payment method used. | [optional] 
**buying_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**ship_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**bill_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**ship_window** | **str** | Defines a date time interval according to ISO8601. Interval is separated by double hyphen (--). | [optional] 
**delivery_window** | **str** | Defines a date time interval according to ISO8601. Interval is separated by double hyphen (--). | [optional] 
**items** | [**List[OrderItem]**](OrderItem.md) | A list of items in this purchase order. | 

## Example

```python
from py_sp_api.generated.vendorOrders.models.order_details import OrderDetails

# TODO update the JSON string below
json = "{}"
# create an instance of OrderDetails from a JSON string
order_details_instance = OrderDetails.from_json(json)
# print the JSON string representation of the object
print(OrderDetails.to_json())

# convert the object into a dict
order_details_dict = order_details_instance.to_dict()
# create an instance of OrderDetails from a dict
order_details_from_dict = OrderDetails.from_dict(order_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


