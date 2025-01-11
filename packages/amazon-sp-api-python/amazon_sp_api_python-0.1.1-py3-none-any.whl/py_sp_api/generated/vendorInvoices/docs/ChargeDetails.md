# ChargeDetails

Monetary and tax details of the charge.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Type of the charge applied. | 
**description** | **str** | Description of the charge. | [optional] 
**charge_amount** | [**Money**](Money.md) |  | 
**tax_details** | [**List[TaxDetails]**](TaxDetails.md) | Tax amount details applied on this charge. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.charge_details import ChargeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ChargeDetails from a JSON string
charge_details_instance = ChargeDetails.from_json(json)
# print the JSON string representation of the object
print(ChargeDetails.to_json())

# convert the object into a dict
charge_details_dict = charge_details_instance.to_dict()
# create an instance of ChargeDetails from a dict
charge_details_from_dict = ChargeDetails.from_dict(charge_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


