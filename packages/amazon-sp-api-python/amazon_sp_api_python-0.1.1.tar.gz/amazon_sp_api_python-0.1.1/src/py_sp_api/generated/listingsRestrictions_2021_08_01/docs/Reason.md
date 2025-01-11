# Reason

A reason for the restriction, including path forward links that may allow Selling Partners to remove the restriction, if available.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A message describing the reason for the restriction. | 
**reason_code** | **str** | A code indicating why the listing is restricted. | [optional] 
**links** | [**List[Link]**](Link.md) | A list of path forward links that may allow Selling Partners to remove the restriction. | [optional] 

## Example

```python
from py_sp_api.generated.listingsRestrictions_2021_08_01.models.reason import Reason

# TODO update the JSON string below
json = "{}"
# create an instance of Reason from a JSON string
reason_instance = Reason.from_json(json)
# print the JSON string representation of the object
print(Reason.to_json())

# convert the object into a dict
reason_dict = reason_instance.to_dict()
# create an instance of Reason from a dict
reason_from_dict = Reason.from_dict(reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


