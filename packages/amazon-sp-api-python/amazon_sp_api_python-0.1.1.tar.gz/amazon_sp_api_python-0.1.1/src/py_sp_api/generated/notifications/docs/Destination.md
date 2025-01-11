# Destination

Information about the destination created when you call the `createDestination` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The developer-defined name for this destination. | 
**destination_id** | **str** | The destination identifier generated when you created the destination. | 
**resource** | [**DestinationResource**](DestinationResource.md) |  | 

## Example

```python
from py_sp_api.generated.notifications.models.destination import Destination

# TODO update the JSON string below
json = "{}"
# create an instance of Destination from a JSON string
destination_instance = Destination.from_json(json)
# print the JSON string representation of the object
print(Destination.to_json())

# convert the object into a dict
destination_dict = destination_instance.to_dict()
# create an instance of Destination from a dict
destination_from_dict = Destination.from_dict(destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


