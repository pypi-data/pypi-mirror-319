# GetDestinationsResponse

The response schema for the `getDestinations` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[Destination]**](Destination.md) | A list of destinations. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.get_destinations_response import GetDestinationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDestinationsResponse from a JSON string
get_destinations_response_instance = GetDestinationsResponse.from_json(json)
# print the JSON string representation of the object
print(GetDestinationsResponse.to_json())

# convert the object into a dict
get_destinations_response_dict = get_destinations_response_instance.to_dict()
# create an instance of GetDestinationsResponse from a dict
get_destinations_response_from_dict = GetDestinationsResponse.from_dict(get_destinations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


