# DeliveryChannel

The delivery channel of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_supported** | **bool** |  | [optional] 
**operational_configuration** | [**OperationalConfiguration**](OperationalConfiguration.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.delivery_channel import DeliveryChannel

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryChannel from a JSON string
delivery_channel_instance = DeliveryChannel.from_json(json)
# print the JSON string representation of the object
print(DeliveryChannel.to_json())

# convert the object into a dict
delivery_channel_dict = delivery_channel_instance.to_dict()
# create an instance of DeliveryChannel from a dict
delivery_channel_from_dict = DeliveryChannel.from_dict(delivery_channel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


