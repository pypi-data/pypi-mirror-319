# Route

This is used only for direct import shipment confirmations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stops** | [**List[Stop]**](Stop.md) | The port or location involved in transporting the cargo, as specified in transportation contracts or operational plans. | 

## Example

```python
from py_sp_api.generated.vendorShipments.models.route import Route

# TODO update the JSON string below
json = "{}"
# create an instance of Route from a JSON string
route_instance = Route.from_json(json)
# print the JSON string representation of the object
print(Route.to_json())

# convert the object into a dict
route_dict = route_instance.to_dict()
# create an instance of Route from a dict
route_from_dict = Route.from_dict(route_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


