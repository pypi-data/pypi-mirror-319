# OutboundCapability

The outbound capability of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_supported** | **bool** |  | [optional] 
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 
**return_location** | [**ReturnLocation**](ReturnLocation.md) |  | [optional] 
**delivery_channel** | [**DeliveryChannel**](DeliveryChannel.md) |  | [optional] 
**pickup_channel** | [**PickupChannel**](PickupChannel.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.outbound_capability import OutboundCapability

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundCapability from a JSON string
outbound_capability_instance = OutboundCapability.from_json(json)
# print the JSON string representation of the object
print(OutboundCapability.to_json())

# convert the object into a dict
outbound_capability_dict = outbound_capability_instance.to_dict()
# create an instance of OutboundCapability from a dict
outbound_capability_from_dict = OutboundCapability.from_dict(outbound_capability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


