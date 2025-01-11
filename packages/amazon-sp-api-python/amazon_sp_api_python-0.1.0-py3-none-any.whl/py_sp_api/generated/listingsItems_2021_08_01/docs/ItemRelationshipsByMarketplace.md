# ItemRelationshipsByMarketplace

Relationship details for the listing item in the specified marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**relationships** | [**List[ItemRelationship]**](ItemRelationship.md) | Relationships for the listing item. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.item_relationships_by_marketplace import ItemRelationshipsByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemRelationshipsByMarketplace from a JSON string
item_relationships_by_marketplace_instance = ItemRelationshipsByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemRelationshipsByMarketplace.to_json())

# convert the object into a dict
item_relationships_by_marketplace_dict = item_relationships_by_marketplace_instance.to_dict()
# create an instance of ItemRelationshipsByMarketplace from a dict
item_relationships_by_marketplace_from_dict = ItemRelationshipsByMarketplace.from_dict(item_relationships_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


