# Image

The image attribute of the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | The image URL attribute of the item. | [optional] 
**height** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**width** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.image import Image

# TODO update the JSON string below
json = "{}"
# create an instance of Image from a JSON string
image_instance = Image.from_json(json)
# print the JSON string representation of the object
print(Image.to_json())

# convert the object into a dict
image_dict = image_instance.to_dict()
# create an instance of Image from a dict
image_from_dict = Image.from_dict(image_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


