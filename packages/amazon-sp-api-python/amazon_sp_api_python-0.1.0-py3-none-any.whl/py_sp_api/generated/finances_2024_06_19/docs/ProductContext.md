# ProductContext

Additional information related to the product.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**sku** | **str** | The Stock Keeping Unit (SKU) of the item. | [optional] 
**quantity_shipped** | **int** | The quantity of the item shipped. | [optional] 
**fulfillment_network** | **str** | The fulfillment network of the item. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.product_context import ProductContext

# TODO update the JSON string below
json = "{}"
# create an instance of ProductContext from a JSON string
product_context_instance = ProductContext.from_json(json)
# print the JSON string representation of the object
print(ProductContext.to_json())

# convert the object into a dict
product_context_dict = product_context_instance.to_dict()
# create an instance of ProductContext from a dict
product_context_from_dict = ProductContext.from_dict(product_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


