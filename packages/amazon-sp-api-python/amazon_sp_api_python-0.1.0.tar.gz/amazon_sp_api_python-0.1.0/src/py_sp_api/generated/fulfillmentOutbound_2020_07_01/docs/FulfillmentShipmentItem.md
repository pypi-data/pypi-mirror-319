# FulfillmentShipmentItem

Item information for a shipment in a fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**seller_fulfillment_order_item_id** | **str** | The fulfillment order item identifier that the seller created and submitted with a call to the &#x60;createFulfillmentOrder&#x60; operation. | 
**quantity** | **int** | The item quantity. | 
**package_number** | **int** | An identifier for the package that contains the item quantity. | [optional] 
**serial_number** | **str** | The serial number of the shipped item. | [optional] 
**manufacturer_lot_codes** | **List[str]** | String list | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.fulfillment_shipment_item import FulfillmentShipmentItem

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentShipmentItem from a JSON string
fulfillment_shipment_item_instance = FulfillmentShipmentItem.from_json(json)
# print the JSON string representation of the object
print(FulfillmentShipmentItem.to_json())

# convert the object into a dict
fulfillment_shipment_item_dict = fulfillment_shipment_item_instance.to_dict()
# create an instance of FulfillmentShipmentItem from a dict
fulfillment_shipment_item_from_dict = FulfillmentShipmentItem.from_dict(fulfillment_shipment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


