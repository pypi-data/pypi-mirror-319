# Error

Error response returned when the request is unsuccessful.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | An error code that identifies the type of error that occurred. | 
**message** | **str** | A message that describes the error condition. | 
**details** | **str** | Additional details that can help the caller understand or fix the issue. | [optional] 

## Example

```python
from py_sp_api.generated.dataKiosk_2023_11_15.models.error import Error

# TODO update the JSON string below
json = "{}"
# create an instance of Error from a JSON string
error_instance = Error.from_json(json)
# print the JSON string representation of the object
print(Error.to_json())

# convert the object into a dict
error_dict = error_instance.to_dict()
# create an instance of Error from a dict
error_from_dict = Error.from_dict(error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


