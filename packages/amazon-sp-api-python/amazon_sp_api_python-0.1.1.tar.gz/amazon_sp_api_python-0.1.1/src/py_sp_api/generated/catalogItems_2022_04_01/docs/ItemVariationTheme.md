# ItemVariationTheme

Variation theme indicating the combination of Amazon item catalog attributes that define the variation family.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | **List[str]** | Names of the Amazon catalog item attributes associated with the variation theme. | [optional] 
**theme** | **str** | Variation theme indicating the combination of Amazon item catalog attributes that define the variation family. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_variation_theme import ItemVariationTheme

# TODO update the JSON string below
json = "{}"
# create an instance of ItemVariationTheme from a JSON string
item_variation_theme_instance = ItemVariationTheme.from_json(json)
# print the JSON string representation of the object
print(ItemVariationTheme.to_json())

# convert the object into a dict
item_variation_theme_dict = item_variation_theme_instance.to_dict()
# create an instance of ItemVariationTheme from a dict
item_variation_theme_from_dict = ItemVariationTheme.from_dict(item_variation_theme_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


