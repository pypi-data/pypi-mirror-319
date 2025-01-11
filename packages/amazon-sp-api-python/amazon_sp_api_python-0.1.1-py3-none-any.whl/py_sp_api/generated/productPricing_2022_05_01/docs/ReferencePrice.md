# ReferencePrice

The reference price for the specified ASIN `marketplaceId` combination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the reference price, such as &#x60;CompetitivePriceThreshold&#x60; and &#x60;WasPrice&#x60;. For reference price definitions, refer to the [Use Case Guide](https://developer-docs.amazon.com/sp-api/docs/product-pricing-api-v2022-05-01-use-case-guide). | 
**price** | [**MoneyType**](MoneyType.md) |  | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.reference_price import ReferencePrice

# TODO update the JSON string below
json = "{}"
# create an instance of ReferencePrice from a JSON string
reference_price_instance = ReferencePrice.from_json(json)
# print the JSON string representation of the object
print(ReferencePrice.to_json())

# convert the object into a dict
reference_price_dict = reference_price_instance.to_dict()
# create an instance of ReferencePrice from a dict
reference_price_from_dict = ReferencePrice.from_dict(reference_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


