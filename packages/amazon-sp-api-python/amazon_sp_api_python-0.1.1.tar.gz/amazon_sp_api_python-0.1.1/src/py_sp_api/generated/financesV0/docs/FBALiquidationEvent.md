# FBALiquidationEvent

A payment event for Fulfillment by Amazon (FBA) inventory liquidation. This event is used only in the US marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**original_removal_order_id** | **str** | The identifier for the original removal order. | [optional] 
**liquidation_proceeds_amount** | [**Currency**](Currency.md) |  | [optional] 
**liquidation_fee_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.fba_liquidation_event import FBALiquidationEvent

# TODO update the JSON string below
json = "{}"
# create an instance of FBALiquidationEvent from a JSON string
fba_liquidation_event_instance = FBALiquidationEvent.from_json(json)
# print the JSON string representation of the object
print(FBALiquidationEvent.to_json())

# convert the object into a dict
fba_liquidation_event_dict = fba_liquidation_event_instance.to_dict()
# create an instance of FBALiquidationEvent from a dict
fba_liquidation_event_from_dict = FBALiquidationEvent.from_dict(fba_liquidation_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


