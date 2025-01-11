# UpdateShipmentStatusRequest

The request body for the `updateShipmentStatus` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The unobfuscated marketplace identifier. | 
**shipment_status** | [**ShipmentStatus**](ShipmentStatus.md) |  | 
**order_items** | [**List[OrderItemsInner]**](OrderItemsInner.md) | For partial shipment status updates, the list of order items and quantities to be updated. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.update_shipment_status_request import UpdateShipmentStatusRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentStatusRequest from a JSON string
update_shipment_status_request_instance = UpdateShipmentStatusRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentStatusRequest.to_json())

# convert the object into a dict
update_shipment_status_request_dict = update_shipment_status_request_instance.to_dict()
# create an instance of UpdateShipmentStatusRequest from a dict
update_shipment_status_request_from_dict = UpdateShipmentStatusRequest.from_dict(update_shipment_status_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


