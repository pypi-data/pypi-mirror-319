# ItemVariationTheme

A variation theme that indicates the combination of listing item attributes that define the variation family.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | **List[str]** | The names of the listing item attributes that are associated with the variation theme. | 
**theme** | **str** | The variation theme that indicates the combination of listing item attributes that define the variation family. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_variation_theme import ItemVariationTheme

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


