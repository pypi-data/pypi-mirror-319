# CreateDestinationResponse

The response schema for the createDestination operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Destination**](Destination.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.create_destination_response import CreateDestinationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDestinationResponse from a JSON string
create_destination_response_instance = CreateDestinationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateDestinationResponse.to_json())

# convert the object into a dict
create_destination_response_dict = create_destination_response_instance.to_dict()
# create an instance of CreateDestinationResponse from a dict
create_destination_response_from_dict = CreateDestinationResponse.from_dict(create_destination_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


