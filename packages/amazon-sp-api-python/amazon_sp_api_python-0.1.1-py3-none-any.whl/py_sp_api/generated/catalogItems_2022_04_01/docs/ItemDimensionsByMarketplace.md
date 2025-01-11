# ItemDimensionsByMarketplace

Dimensions associated with the item in the Amazon catalog for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**item** | [**Dimensions**](Dimensions.md) |  | [optional] 
**package** | [**Dimensions**](Dimensions.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_dimensions_by_marketplace import ItemDimensionsByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemDimensionsByMarketplace from a JSON string
item_dimensions_by_marketplace_instance = ItemDimensionsByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemDimensionsByMarketplace.to_json())

# convert the object into a dict
item_dimensions_by_marketplace_dict = item_dimensions_by_marketplace_instance.to_dict()
# create an instance of ItemDimensionsByMarketplace from a dict
item_dimensions_by_marketplace_from_dict = ItemDimensionsByMarketplace.from_dict(item_dimensions_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


