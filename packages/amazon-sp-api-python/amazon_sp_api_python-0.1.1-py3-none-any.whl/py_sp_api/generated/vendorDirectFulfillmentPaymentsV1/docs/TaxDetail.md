# TaxDetail

Details of tax amount applied.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_type** | **str** | Type of the tax applied. | 
**tax_rate** | **str** | A decimal number with no loss of precision. Useful when precision loss is unacceptable, as with currencies. Follows RFC7159 for number representation. &lt;br&gt;**Pattern** : &#x60;^-?(0|([1-9]\\d*))(\\.\\d+)?([eE][+-]?\\d+)?$&#x60;. | [optional] 
**tax_amount** | [**Money**](Money.md) |  | 
**taxable_amount** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.tax_detail import TaxDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TaxDetail from a JSON string
tax_detail_instance = TaxDetail.from_json(json)
# print the JSON string representation of the object
print(TaxDetail.to_json())

# convert the object into a dict
tax_detail_dict = tax_detail_instance.to_dict()
# create an instance of TaxDetail from a dict
tax_detail_from_dict = TaxDetail.from_dict(tax_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


