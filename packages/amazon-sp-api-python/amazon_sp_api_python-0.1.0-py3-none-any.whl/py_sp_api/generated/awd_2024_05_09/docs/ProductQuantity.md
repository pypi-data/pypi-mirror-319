# ProductQuantity

Represents a product with the SKU details and the corresponding quantity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**List[ProductAttribute]**](ProductAttribute.md) | Attributes for this instance of the product. For example, already-prepped, or other attributes that distinguish the product beyond the SKU. | [optional] 
**quantity** | **int** | Product quantity. | 
**sku** | **str** | The seller or merchant SKU. | 
**expiration** | **datetime** | The expiration date for the SKU. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**prep_details** | [**PrepDetails**](PrepDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.product_quantity import ProductQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of ProductQuantity from a JSON string
product_quantity_instance = ProductQuantity.from_json(json)
# print the JSON string representation of the object
print(ProductQuantity.to_json())

# convert the object into a dict
product_quantity_dict = product_quantity_instance.to_dict()
# create an instance of ProductQuantity from a dict
product_quantity_from_dict = ProductQuantity.from_dict(product_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


