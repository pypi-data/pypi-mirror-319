# CreateDestinationRequest

The request schema for the `createDestination` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_specification** | [**DestinationResourceSpecification**](DestinationResourceSpecification.md) |  | 
**name** | **str** | A developer-defined name to help identify this destination. | 

## Example

```python
from py_sp_api.generated.notifications.models.create_destination_request import CreateDestinationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDestinationRequest from a JSON string
create_destination_request_instance = CreateDestinationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDestinationRequest.to_json())

# convert the object into a dict
create_destination_request_dict = create_destination_request_instance.to_dict()
# create an instance of CreateDestinationRequest from a dict
create_destination_request_from_dict = CreateDestinationRequest.from_dict(create_destination_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


