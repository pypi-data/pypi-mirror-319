# ParkingConfiguration

The parking configuration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parking_cost_type** | [**ParkingCostType**](ParkingCostType.md) |  | [optional] 
**parking_spot_identification_type** | [**ParkingSpotIdentificationType**](ParkingSpotIdentificationType.md) |  | [optional] 
**number_of_parking_spots** | **int** | An unsigned integer that can be only positive or zero. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.parking_configuration import ParkingConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of ParkingConfiguration from a JSON string
parking_configuration_instance = ParkingConfiguration.from_json(json)
# print the JSON string representation of the object
print(ParkingConfiguration.to_json())

# convert the object into a dict
parking_configuration_dict = parking_configuration_instance.to_dict()
# create an instance of ParkingConfiguration from a dict
parking_configuration_from_dict = ParkingConfiguration.from_dict(parking_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


