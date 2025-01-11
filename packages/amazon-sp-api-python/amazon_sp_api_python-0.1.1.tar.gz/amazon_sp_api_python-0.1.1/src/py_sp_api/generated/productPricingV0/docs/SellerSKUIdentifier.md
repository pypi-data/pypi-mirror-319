# SellerSKUIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. | 
**seller_id** | **str** | The seller identifier submitted for the operation. | 
**seller_sku** | **str** | The seller stock keeping unit (SKU) of the item. | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.seller_sku_identifier import SellerSKUIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of SellerSKUIdentifier from a JSON string
seller_sku_identifier_instance = SellerSKUIdentifier.from_json(json)
# print the JSON string representation of the object
print(SellerSKUIdentifier.to_json())

# convert the object into a dict
seller_sku_identifier_dict = seller_sku_identifier_instance.to_dict()
# create an instance of SellerSKUIdentifier from a dict
seller_sku_identifier_from_dict = SellerSKUIdentifier.from_dict(seller_sku_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


