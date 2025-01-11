# DeleteDestinationResponse

The response schema for the `deleteDestination` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.delete_destination_response import DeleteDestinationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteDestinationResponse from a JSON string
delete_destination_response_instance = DeleteDestinationResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteDestinationResponse.to_json())

# convert the object into a dict
delete_destination_response_dict = delete_destination_response_instance.to_dict()
# create an instance of DeleteDestinationResponse from a dict
delete_destination_response_from_dict = DeleteDestinationResponse.from_dict(delete_destination_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


