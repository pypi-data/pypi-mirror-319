# AplusResponse

The base response data for all A+ Content operations when a request is successful or partially successful. Individual operations may extend this with additional data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.aplus_response import AplusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AplusResponse from a JSON string
aplus_response_instance = AplusResponse.from_json(json)
# print the JSON string representation of the object
print(AplusResponse.to_json())

# convert the object into a dict
aplus_response_dict = aplus_response_instance.to_dict()
# create an instance of AplusResponse from a dict
aplus_response_from_dict = AplusResponse.from_dict(aplus_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


