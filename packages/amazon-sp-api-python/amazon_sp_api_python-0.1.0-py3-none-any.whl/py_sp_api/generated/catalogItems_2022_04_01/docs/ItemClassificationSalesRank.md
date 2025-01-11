# ItemClassificationSalesRank

Sales rank of an Amazon catalog item by classification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_id** | **str** | Identifier of the classification associated with the sales rank. | 
**title** | **str** | Title, or name, of the sales rank. | 
**link** | **str** | Corresponding Amazon retail website link, or URL, for the sales rank. | [optional] 
**rank** | **int** | Sales rank value. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_classification_sales_rank import ItemClassificationSalesRank

# TODO update the JSON string below
json = "{}"
# create an instance of ItemClassificationSalesRank from a JSON string
item_classification_sales_rank_instance = ItemClassificationSalesRank.from_json(json)
# print the JSON string representation of the object
print(ItemClassificationSalesRank.to_json())

# convert the object into a dict
item_classification_sales_rank_dict = item_classification_sales_rank_instance.to_dict()
# create an instance of ItemClassificationSalesRank from a dict
item_classification_sales_rank_from_dict = ItemClassificationSalesRank.from_dict(item_classification_sales_rank_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


