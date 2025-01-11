# TaxRate

Contains the type and rate of tax.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cess_rate** | **float** | Rate of cess tax. | [optional] 
**gst_rate** | **float** | Rate of gst tax. | [optional] 
**tax_type** | **str** | Type of tax. Possible values: &#x60;CGST&#x60;, &#x60;SGST&#x60;, &#x60;IGST&#x60;, &#x60;TOTAL_TAX&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.tax_rate import TaxRate

# TODO update the JSON string below
json = "{}"
# create an instance of TaxRate from a JSON string
tax_rate_instance = TaxRate.from_json(json)
# print the JSON string representation of the object
print(TaxRate.to_json())

# convert the object into a dict
tax_rate_dict = tax_rate_instance.to_dict()
# create an instance of TaxRate from a dict
tax_rate_from_dict = TaxRate.from_dict(tax_rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


