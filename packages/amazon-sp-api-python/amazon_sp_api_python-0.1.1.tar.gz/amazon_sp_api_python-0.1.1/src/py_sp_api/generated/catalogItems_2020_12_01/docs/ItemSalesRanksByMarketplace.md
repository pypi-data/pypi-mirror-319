# ItemSalesRanksByMarketplace

Sales ranks of an Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**ranks** | [**List[ItemSalesRank]**](ItemSalesRank.md) | Sales ranks of an Amazon catalog item for an Amazon marketplace. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_sales_ranks_by_marketplace import ItemSalesRanksByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemSalesRanksByMarketplace from a JSON string
item_sales_ranks_by_marketplace_instance = ItemSalesRanksByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemSalesRanksByMarketplace.to_json())

# convert the object into a dict
item_sales_ranks_by_marketplace_dict = item_sales_ranks_by_marketplace_instance.to_dict()
# create an instance of ItemSalesRanksByMarketplace from a dict
item_sales_ranks_by_marketplace_from_dict = ItemSalesRanksByMarketplace.from_dict(item_sales_ranks_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


