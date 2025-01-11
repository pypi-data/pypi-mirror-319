# PickupChannel

The pick up channel of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inventory_hold_period** | [**Duration**](Duration.md) |  | [optional] 
**is_supported** | **bool** |  | [optional] 
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 
**in_store_pickup_configuration** | [**InStorePickupConfiguration**](InStorePickupConfiguration.md) |  | [optional] 
**curbside_pickup_configuration** | [**CurbsidePickupConfiguration**](CurbsidePickupConfiguration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.pickup_channel import PickupChannel

# TODO update the JSON string below
json = "{}"
# create an instance of PickupChannel from a JSON string
pickup_channel_instance = PickupChannel.from_json(json)
# print the JSON string representation of the object
print(PickupChannel.to_json())

# convert the object into a dict
pickup_channel_dict = pickup_channel_instance.to_dict()
# create an instance of PickupChannel from a dict
pickup_channel_from_dict = PickupChannel.from_dict(pickup_channel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


