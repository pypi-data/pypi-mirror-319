# Issue

An issue with a listings item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | An issue code that identifies the type of issue. | 
**message** | **str** | A message that describes the issue. | 
**severity** | **str** | The severity of the issue. | 
**attribute_name** | **str** | Name of the attribute associated with the issue, if applicable. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2020_09_01.models.issue import Issue

# TODO update the JSON string below
json = "{}"
# create an instance of Issue from a JSON string
issue_instance = Issue.from_json(json)
# print the JSON string representation of the object
print(Issue.to_json())

# convert the object into a dict
issue_dict = issue_instance.to_dict()
# create an instance of Issue from a dict
issue_from_dict = Issue.from_dict(issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


