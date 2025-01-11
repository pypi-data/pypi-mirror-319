# Item

An item in the Amazon catalog.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifiers** | [**IdentifierType**](IdentifierType.md) |  | 
**attribute_sets** | [**List[AttributeSetListType]**](AttributeSetListType.md) | A list of attributes for the item. | [optional] 
**relationships** | [**List[RelationshipType]**](RelationshipType.md) | A list of variation relationship information, if applicable for the item. | [optional] 
**sales_rankings** | [**List[SalesRankType]**](SalesRankType.md) | A list of sales rank information for the item by category. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.item import Item

# TODO update the JSON string below
json = "{}"
# create an instance of Item from a JSON string
item_instance = Item.from_json(json)
# print the JSON string representation of the object
print(Item.to_json())

# convert the object into a dict
item_dict = item_instance.to_dict()
# create an instance of Item from a dict
item_from_dict = Item.from_dict(item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


