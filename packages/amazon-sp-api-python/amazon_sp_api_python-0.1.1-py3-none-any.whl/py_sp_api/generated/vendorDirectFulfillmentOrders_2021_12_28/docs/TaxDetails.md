# TaxDetails

The tax details related to the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_rate** | **str** | A decimal number with no loss of precision. Useful when precision loss is unacceptable, as with currencies. Follows RFC7159 for number representation. | [optional] 
**tax_amount** | [**Money**](Money.md) |  | 
**taxable_amount** | [**Money**](Money.md) |  | [optional] 
**type** | **str** | Tax type. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.tax_details import TaxDetails

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


