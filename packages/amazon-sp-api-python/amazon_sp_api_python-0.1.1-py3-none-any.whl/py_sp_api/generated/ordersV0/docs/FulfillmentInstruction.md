# FulfillmentInstruction

Contains the instructions about the fulfillment, such as the location from where you want the order filled.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_supply_source_id** | **str** | The &#x60;sourceId&#x60; of the location from where you want the order fulfilled. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.fulfillment_instruction import FulfillmentInstruction

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentInstruction from a JSON string
fulfillment_instruction_instance = FulfillmentInstruction.from_json(json)
# print the JSON string representation of the object
print(FulfillmentInstruction.to_json())

# convert the object into a dict
fulfillment_instruction_dict = fulfillment_instruction_instance.to_dict()
# create an instance of FulfillmentInstruction from a dict
fulfillment_instruction_from_dict = FulfillmentInstruction.from_dict(fulfillment_instruction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


