# RemovalShipmentAdjustmentEvent

A financial adjustment event for FBA liquidated inventory. A positive value indicates money owed to Amazon by the buyer (for example, when the charge was incorrectly calculated as less than it should be). A negative value indicates a full or partial refund owed to the buyer (for example, when the buyer receives damaged items or fewer items than ordered).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**adjustment_event_id** | **str** | The unique identifier for the adjustment event. | [optional] 
**merchant_order_id** | **str** | The merchant removal orderId. | [optional] 
**order_id** | **str** | The orderId for shipping inventory. | [optional] 
**transaction_type** | **str** | The type of removal order.  Possible values:  * WHOLESALE_LIQUIDATION. | [optional] 
**removal_shipment_item_adjustment_list** | [**List[RemovalShipmentItemAdjustment]**](RemovalShipmentItemAdjustment.md) | A comma-delimited list of Removal shipmentItemAdjustment details for FBA inventory. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.removal_shipment_adjustment_event import RemovalShipmentAdjustmentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of RemovalShipmentAdjustmentEvent from a JSON string
removal_shipment_adjustment_event_instance = RemovalShipmentAdjustmentEvent.from_json(json)
# print the JSON string representation of the object
print(RemovalShipmentAdjustmentEvent.to_json())

# convert the object into a dict
removal_shipment_adjustment_event_dict = removal_shipment_adjustment_event_instance.to_dict()
# create an instance of RemovalShipmentAdjustmentEvent from a dict
removal_shipment_adjustment_event_from_dict = RemovalShipmentAdjustmentEvent.from_dict(removal_shipment_adjustment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


