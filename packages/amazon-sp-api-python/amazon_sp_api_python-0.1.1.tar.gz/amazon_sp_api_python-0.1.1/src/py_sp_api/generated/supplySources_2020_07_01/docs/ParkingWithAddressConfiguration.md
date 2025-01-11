# ParkingWithAddressConfiguration

The parking configuration with the address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parking_cost_type** | [**ParkingCostType**](ParkingCostType.md) |  | [optional] 
**parking_spot_identification_type** | [**ParkingSpotIdentificationType**](ParkingSpotIdentificationType.md) |  | [optional] 
**number_of_parking_spots** | **int** | An unsigned integer that can be only positive or zero. | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.parking_with_address_configuration import ParkingWithAddressConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of ParkingWithAddressConfiguration from a JSON string
parking_with_address_configuration_instance = ParkingWithAddressConfiguration.from_json(json)
# print the JSON string representation of the object
print(ParkingWithAddressConfiguration.to_json())

# convert the object into a dict
parking_with_address_configuration_dict = parking_with_address_configuration_instance.to_dict()
# create an instance of ParkingWithAddressConfiguration from a dict
parking_with_address_configuration_from_dict = ParkingWithAddressConfiguration.from_dict(parking_with_address_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


