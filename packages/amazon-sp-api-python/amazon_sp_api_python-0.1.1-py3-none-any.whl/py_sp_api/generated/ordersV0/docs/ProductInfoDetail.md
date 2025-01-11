# ProductInfoDetail

Product information on the number of items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_items** | **str** | The total number of items that are included in the ASIN. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.product_info_detail import ProductInfoDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ProductInfoDetail from a JSON string
product_info_detail_instance = ProductInfoDetail.from_json(json)
# print the JSON string representation of the object
print(ProductInfoDetail.to_json())

# convert the object into a dict
product_info_detail_dict = product_info_detail_instance.to_dict()
# create an instance of ProductInfoDetail from a dict
product_info_detail_from_dict = ProductInfoDetail.from_dict(product_info_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


