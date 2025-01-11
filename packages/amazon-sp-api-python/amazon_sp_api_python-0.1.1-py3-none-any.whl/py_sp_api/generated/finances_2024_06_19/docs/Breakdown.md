# Breakdown

Details about the movement of money in the financial transaction. Breakdowns are further categorized into breakdown types, breakdown amounts, and further breakdowns.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**breakdown_type** | **str** | The type of charge. | [optional] 
**breakdown_amount** | [**Currency**](Currency.md) |  | [optional] 
**breakdowns** | [**Breakdown**](Breakdown.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.breakdown import Breakdown

# TODO update the JSON string below
json = "{}"
# create an instance of Breakdown from a JSON string
breakdown_instance = Breakdown.from_json(json)
# print the JSON string representation of the object
print(Breakdown.to_json())

# convert the object into a dict
breakdown_dict = breakdown_instance.to_dict()
# create an instance of Breakdown from a dict
breakdown_from_dict = Breakdown.from_dict(breakdown_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


