# RemovalShipmentEvent

A removal shipment event for a removal order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**merchant_order_id** | **str** | The merchant removal orderId. | [optional] 
**order_id** | **str** | The identifier for the removal shipment order. | [optional] 
**transaction_type** | **str** | The type of removal order.  Possible values:  * WHOLESALE_LIQUIDATION | [optional] 
**store_name** | **str** | The name of the store where the event occurred. | [optional] 
**removal_shipment_item_list** | [**List[RemovalShipmentItem]**](RemovalShipmentItem.md) | A list of information about removal shipment items. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.removal_shipment_event import RemovalShipmentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RemovalShipmentEvent from a JSON string
removal_shipment_event_instance = RemovalShipmentEvent.from_json(json)
# print the JSON string representation of the object
print(RemovalShipmentEvent.to_json())

# convert the object into a dict
removal_shipment_event_dict = removal_shipment_event_instance.to_dict()
# create an instance of RemovalShipmentEvent from a dict
removal_shipment_event_from_dict = RemovalShipmentEvent.from_dict(removal_shipment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


