# Stop

Contractual or operational port or point relevant to the movement of the cargo.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_code** | **str** | Provide the function code. | 
**location_identification** | [**Location**](Location.md) |  | [optional] 
**arrival_time** | **datetime** | Date and time of the arrival of the cargo. | [optional] 
**departure_time** | **datetime** | Date and time of the departure of the cargo. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.stop import Stop

# TODO update the JSON string below
json = "{}"
# create an instance of Stop from a JSON string
stop_instance = Stop.from_json(json)
# print the JSON string representation of the object
print(Stop.to_json())

# convert the object into a dict
stop_dict = stop_instance.to_dict()
# create an instance of Stop from a dict
stop_from_dict = Stop.from_dict(stop_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


