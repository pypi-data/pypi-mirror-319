# TaxDetails

Information used to determine the tax compliance.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**declared_value** | [**Currency**](Currency.md) |  | [optional] 
**hsn_code** | **str** | Harmonized System of Nomenclature code. | [optional] 
**tax_rates** | [**List[TaxRate]**](TaxRate.md) | List of tax rates. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.tax_details import TaxDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TaxDetails from a JSON string
tax_details_instance = TaxDetails.from_json(json)
# print the JSON string representation of the object
print(TaxDetails.to_json())

# convert the object into a dict
tax_details_dict = tax_details_instance.to_dict()
# create an instance of TaxDetails from a dict
tax_details_from_dict = TaxDetails.from_dict(tax_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


