# MarketplaceTaxInfo

Tax information about the marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_classifications** | [**List[TaxClassification]**](TaxClassification.md) | A list of tax classifications that apply to the order. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.marketplace_tax_info import MarketplaceTaxInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MarketplaceTaxInfo from a JSON string
marketplace_tax_info_instance = MarketplaceTaxInfo.from_json(json)
# print the JSON string representation of the object
print(MarketplaceTaxInfo.to_json())

# convert the object into a dict
marketplace_tax_info_dict = marketplace_tax_info_instance.to_dict()
# create an instance of MarketplaceTaxInfo from a dict
marketplace_tax_info_from_dict = MarketplaceTaxInfo.from_dict(marketplace_tax_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


