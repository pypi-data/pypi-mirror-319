# Restriction

A listing restriction, optionally qualified by a condition, with a list of reasons for the restriction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Identifies the Amazon marketplace where the restriction is enforced. | 
**condition_type** | **str** | The condition that applies to the restriction. | [optional] 
**reasons** | [**List[Reason]**](Reason.md) | A list of reasons for the restriction. | [optional] 

## Example

```python
from py_sp_api.generated.listingsRestrictions_2021_08_01.models.restriction import Restriction

# TODO update the JSON string below
json = "{}"
# create an instance of Restriction from a JSON string
restriction_instance = Restriction.from_json(json)
# print the JSON string representation of the object
print(Restriction.to_json())

# convert the object into a dict
restriction_dict = restriction_instance.to_dict()
# create an instance of Restriction from a dict
restriction_from_dict = Restriction.from_dict(restriction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


