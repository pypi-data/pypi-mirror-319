# ConfirmShipmentOrderItem

A single order item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_item_id** | **str** | The order item&#39;s unique identifier. | 
**quantity** | **int** | The item&#39;s quantity. | 
**transparency_codes** | **List[str]** | A list of order items. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.confirm_shipment_order_item import ConfirmShipmentOrderItem

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmShipmentOrderItem from a JSON string
confirm_shipment_order_item_instance = ConfirmShipmentOrderItem.from_json(json)
# print the JSON string representation of the object
print(ConfirmShipmentOrderItem.to_json())

# convert the object into a dict
confirm_shipment_order_item_dict = confirm_shipment_order_item_instance.to_dict()
# create an instance of ConfirmShipmentOrderItem from a dict
confirm_shipment_order_item_from_dict = ConfirmShipmentOrderItem.from_dict(confirm_shipment_order_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


