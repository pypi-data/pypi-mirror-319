# RestrictionList

A list of restrictions for the specified Amazon catalog item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**restrictions** | [**List[Restriction]**](Restriction.md) |  | 

## Example

```python
from py_sp_api.generated.listingsRestrictions_2021_08_01.models.restriction_list import RestrictionList

# TODO update the JSON string below
json = "{}"
# create an instance of RestrictionList from a JSON string
restriction_list_instance = RestrictionList.from_json(json)
# print the JSON string representation of the object
print(RestrictionList.to_json())

# convert the object into a dict
restriction_list_dict = restriction_list_instance.to_dict()
# create an instance of RestrictionList from a dict
restriction_list_from_dict = RestrictionList.from_dict(restriction_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


