# Warning

Warning returned when the request is successful, but there are important callouts based on which API clients should take defined actions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | An warning code that identifies the type of warning that occurred. | 
**message** | **str** | A message that describes the warning condition in a human-readable form. | 
**details** | **str** | Additional details that can help the caller understand or address the warning. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.warning import Warning

# TODO update the JSON string below
json = "{}"
# create an instance of Warning from a JSON string
warning_instance = Warning.from_json(json)
# print the JSON string representation of the object
print(Warning.to_json())

# convert the object into a dict
warning_dict = warning_instance.to_dict()
# create an instance of Warning from a dict
warning_from_dict = Warning.from_dict(warning_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


