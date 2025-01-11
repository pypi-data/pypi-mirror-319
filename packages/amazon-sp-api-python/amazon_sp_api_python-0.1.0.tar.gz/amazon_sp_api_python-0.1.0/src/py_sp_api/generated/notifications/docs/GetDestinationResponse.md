# GetDestinationResponse

The response schema for the `getDestination` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Destination**](Destination.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.get_destination_response import GetDestinationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDestinationResponse from a JSON string
get_destination_response_instance = GetDestinationResponse.from_json(json)
# print the JSON string representation of the object
print(GetDestinationResponse.to_json())

# convert the object into a dict
get_destination_response_dict = get_destination_response_instance.to_dict()
# create an instance of GetDestinationResponse from a dict
get_destination_response_from_dict = GetDestinationResponse.from_dict(get_destination_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


