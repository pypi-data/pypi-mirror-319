# LiquidVolume

Liquid Volume.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit** | **str** | The unit of measurement. | 
**value** | **float** | The measurement value. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.liquid_volume import LiquidVolume

# TODO update the JSON string below
json = "{}"
# create an instance of LiquidVolume from a JSON string
liquid_volume_instance = LiquidVolume.from_json(json)
# print the JSON string representation of the object
print(LiquidVolume.to_json())

# convert the object into a dict
liquid_volume_dict = liquid_volume_instance.to_dict()
# create an instance of LiquidVolume from a dict
liquid_volume_from_dict = LiquidVolume.from_dict(liquid_volume_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


