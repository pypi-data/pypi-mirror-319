# SalesRankType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_category_id** | **str** | Identifies the item category from which the sales rank is taken. | 
**rank** | **int** | The sales rank of the item within the item category. | 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.sales_rank_type import SalesRankType

# TODO update the JSON string below
json = "{}"
# create an instance of SalesRankType from a JSON string
sales_rank_type_instance = SalesRankType.from_json(json)
# print the JSON string representation of the object
print(SalesRankType.to_json())

# convert the object into a dict
sales_rank_type_dict = sales_rank_type_instance.to_dict()
# create an instance of SalesRankType from a dict
sales_rank_type_from_dict = SalesRankType.from_dict(sales_rank_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


