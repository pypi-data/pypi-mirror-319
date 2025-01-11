# ItemSalesRank

Sales rank of an Amazon catalog item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Title, or name, of the sales rank. | 
**link** | **str** | Corresponding Amazon retail website link, or URL, for the sales rank. | [optional] 
**rank** | **int** | Sales rank value. | 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item_sales_rank import ItemSalesRank

# TODO update the JSON string below
json = "{}"
# create an instance of ItemSalesRank from a JSON string
item_sales_rank_instance = ItemSalesRank.from_json(json)
# print the JSON string representation of the object
print(ItemSalesRank.to_json())

# convert the object into a dict
item_sales_rank_dict = item_sales_rank_instance.to_dict()
# create an instance of ItemSalesRank from a dict
item_sales_rank_from_dict = ItemSalesRank.from_dict(item_sales_rank_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


