# LanguageType

The language type attribute of an item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name attribute of the item. | [optional] 
**type** | **str** | The type attribute of the item. | [optional] 
**audio_format** | **str** | The audio format attribute of the item. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.language_type import LanguageType

# TODO update the JSON string below
json = "{}"
# create an instance of LanguageType from a JSON string
language_type_instance = LanguageType.from_json(json)
# print the JSON string representation of the object
print(LanguageType.to_json())

# convert the object into a dict
language_type_dict = language_type_instance.to_dict()
# create an instance of LanguageType from a dict
language_type_from_dict = LanguageType.from_dict(language_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


