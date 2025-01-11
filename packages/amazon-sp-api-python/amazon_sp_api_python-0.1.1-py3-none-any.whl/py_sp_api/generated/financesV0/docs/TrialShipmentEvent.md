# TrialShipmentEvent

An event related to a trial shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**financial_event_group_id** | **str** | The identifier of the financial event group. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**sku** | **str** | The seller SKU of the item. The seller SKU is qualified by the seller&#39;s seller ID, which is included with every call to the Selling Partner API. | [optional] 
**fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.trial_shipment_event import TrialShipmentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of TrialShipmentEvent from a JSON string
trial_shipment_event_instance = TrialShipmentEvent.from_json(json)
# print the JSON string representation of the object
print(TrialShipmentEvent.to_json())

# convert the object into a dict
trial_shipment_event_dict = trial_shipment_event_instance.to_dict()
# create an instance of TrialShipmentEvent from a dict
trial_shipment_event_from_dict = TrialShipmentEvent.from_dict(trial_shipment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


