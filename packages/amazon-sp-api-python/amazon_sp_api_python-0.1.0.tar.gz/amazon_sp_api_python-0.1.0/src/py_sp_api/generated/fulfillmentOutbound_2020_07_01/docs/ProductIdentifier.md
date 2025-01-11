# ProductIdentifier

Product identifier input that locates a product for MCF.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_sku** | **str** | The merchant SKU for the product. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.product_identifier import ProductIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ProductIdentifier from a JSON string
product_identifier_instance = ProductIdentifier.from_json(json)
# print the JSON string representation of the object
print(ProductIdentifier.to_json())

# convert the object into a dict
product_identifier_dict = product_identifier_instance.to_dict()
# create an instance of ProductIdentifier from a dict
product_identifier_from_dict = ProductIdentifier.from_dict(product_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


