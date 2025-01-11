# ItemRelationship

the relationship details for a listing item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**child_skus** | **List[str]** | Identifiers (SKUs) of the related items that are children of this listing item. | [optional] 
**parent_skus** | **List[str]** | Identifiers (SKUs) of the related items that are parents of this listing item. | [optional] 
**variation_theme** | [**ItemVariationTheme**](ItemVariationTheme.md) |  | [optional] 
**type** | **str** | The type of relationship. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_relationship import ItemRelationship

# TODO update the JSON string below
json = "{}"
# create an instance of ItemRelationship from a JSON string
item_relationship_instance = ItemRelationship.from_json(json)
# print the JSON string representation of the object
print(ItemRelationship.to_json())

# convert the object into a dict
item_relationship_dict = item_relationship_instance.to_dict()
# create an instance of ItemRelationship from a dict
item_relationship_from_dict = ItemRelationship.from_dict(item_relationship_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


