# OrderDetails

Details of an order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_order_number** | **str** | The customer order number. | 
**order_date** | **datetime** | The date the order was placed. This  field is expected to be in ISO-8601 date/time format, for example:2018-07-16T23:00:00Z/ 2018-07-16T23:00:00-05:00 /2018-07-16T23:00:00-08:00. If no time zone is specified, UTC should be assumed. | 
**order_status** | **str** | Current status of the order. | [optional] 
**shipment_details** | [**ShipmentDetails**](ShipmentDetails.md) |  | 
**tax_total** | [**TaxItemDetails**](TaxItemDetails.md) |  | [optional] 
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_to_party** | [**Address**](Address.md) |  | 
**bill_to_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**items** | [**List[OrderItem]**](OrderItem.md) | A list of items in this purchase order. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.order_details import OrderDetails

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


