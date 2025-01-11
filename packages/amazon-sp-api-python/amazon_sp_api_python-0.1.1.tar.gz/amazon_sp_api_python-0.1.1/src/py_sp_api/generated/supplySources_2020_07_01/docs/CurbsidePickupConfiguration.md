# CurbsidePickupConfiguration

The curbside pickup configuration of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_supported** | **bool** | When true, curbside pickup is supported by the supply source. | [optional] 
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 
**parking_with_address_configuration** | [**ParkingWithAddressConfiguration**](ParkingWithAddressConfiguration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.curbside_pickup_configuration import CurbsidePickupConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of CurbsidePickupConfiguration from a JSON string
curbside_pickup_configuration_instance = CurbsidePickupConfiguration.from_json(json)
# print the JSON string representation of the object
print(CurbsidePickupConfiguration.to_json())

# convert the object into a dict
curbside_pickup_configuration_dict = curbside_pickup_configuration_instance.to_dict()
# create an instance of CurbsidePickupConfiguration from a dict
curbside_pickup_configuration_from_dict = CurbsidePickupConfiguration.from_dict(curbside_pickup_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


