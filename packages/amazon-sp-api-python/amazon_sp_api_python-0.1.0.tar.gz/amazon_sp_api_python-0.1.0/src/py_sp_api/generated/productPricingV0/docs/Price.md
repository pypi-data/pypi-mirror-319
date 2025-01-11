# Price


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The status of the operation. | 
**seller_sku** | **str** | The seller stock keeping unit (SKU) of the item. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**product** | [**Product**](Product.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.price import Price

# TODO update the JSON string below
json = "{}"
# create an instance of Price from a JSON string
price_instance = Price.from_json(json)
# print the JSON string representation of the object
print(Price.to_json())

# convert the object into a dict
price_dict = price_instance.to_dict()
# create an instance of Price from a dict
price_from_dict = Price.from_dict(price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


