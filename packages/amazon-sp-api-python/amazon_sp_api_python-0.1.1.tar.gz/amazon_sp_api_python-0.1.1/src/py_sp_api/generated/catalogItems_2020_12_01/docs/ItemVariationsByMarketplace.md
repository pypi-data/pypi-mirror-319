# ItemVariationsByMarketplace

Variation details for the Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**asins** | **List[str]** | Identifiers (ASINs) of the related items. | 
**variation_type** | **str** | Type of variation relationship of the Amazon catalog item in the request to the related item(s): \&quot;PARENT\&quot; or \&quot;CHILD\&quot;. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_variations_by_marketplace import ItemVariationsByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemVariationsByMarketplace from a JSON string
item_variations_by_marketplace_instance = ItemVariationsByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemVariationsByMarketplace.to_json())

# convert the object into a dict
item_variations_by_marketplace_dict = item_variations_by_marketplace_instance.to_dict()
# create an instance of ItemVariationsByMarketplace from a dict
item_variations_by_marketplace_from_dict = ItemVariationsByMarketplace.from_dict(item_variations_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


