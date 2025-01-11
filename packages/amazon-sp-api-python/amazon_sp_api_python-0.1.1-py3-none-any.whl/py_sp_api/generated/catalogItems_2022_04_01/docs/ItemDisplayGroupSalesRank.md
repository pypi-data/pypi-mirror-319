# ItemDisplayGroupSalesRank

Sales rank of an Amazon catalog item by website display group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**website_display_group** | **str** | Name of the website display group associated with the sales rank | 
**title** | **str** | Title, or name, of the sales rank. | 
**link** | **str** | Corresponding Amazon retail website link, or URL, for the sales rank. | [optional] 
**rank** | **int** | Sales rank value. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_display_group_sales_rank import ItemDisplayGroupSalesRank

# TODO update the JSON string below
json = "{}"
# create an instance of ItemDisplayGroupSalesRank from a JSON string
item_display_group_sales_rank_instance = ItemDisplayGroupSalesRank.from_json(json)
# print the JSON string representation of the object
print(ItemDisplayGroupSalesRank.to_json())

# convert the object into a dict
item_display_group_sales_rank_dict = item_display_group_sales_rank_instance.to_dict()
# create an instance of ItemDisplayGroupSalesRank from a dict
item_display_group_sales_rank_from_dict = ItemDisplayGroupSalesRank.from_dict(item_display_group_sales_rank_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


