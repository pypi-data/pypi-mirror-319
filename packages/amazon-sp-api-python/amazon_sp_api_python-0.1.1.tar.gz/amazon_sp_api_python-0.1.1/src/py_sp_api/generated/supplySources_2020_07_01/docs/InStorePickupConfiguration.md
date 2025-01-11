# InStorePickupConfiguration

The in-store pickup configuration of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_supported** | **bool** | When true, in-store pickup is supported by the supply source (default: &#x60;isSupported&#x60; value in &#x60;PickupChannel&#x60;). | [optional] 
**parking_configuration** | [**ParkingConfiguration**](ParkingConfiguration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.in_store_pickup_configuration import InStorePickupConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of InStorePickupConfiguration from a JSON string
in_store_pickup_configuration_instance = InStorePickupConfiguration.from_json(json)
# print the JSON string representation of the object
print(InStorePickupConfiguration.to_json())

# convert the object into a dict
in_store_pickup_configuration_dict = in_store_pickup_configuration_instance.to_dict()
# create an instance of InStorePickupConfiguration from a dict
in_store_pickup_configuration_from_dict = InStorePickupConfiguration.from_dict(in_store_pickup_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


