# TaxRegistrationDetail

Tax registration details of the entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_registration_type** | **str** | Tax registration type for the entity. | [optional] 
**tax_registration_number** | **str** | Tax registration number for the entity. For example, VAT ID, Consumption Tax ID. | 
**tax_registration_address** | [**Address**](Address.md) |  | [optional] 
**tax_registration_message** | **str** | Tax registration message that can be used for additional tax related details. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.tax_registration_detail import TaxRegistrationDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TaxRegistrationDetail from a JSON string
tax_registration_detail_instance = TaxRegistrationDetail.from_json(json)
# print the JSON string representation of the object
print(TaxRegistrationDetail.to_json())

# convert the object into a dict
tax_registration_detail_dict = tax_registration_detail_instance.to_dict()
# create an instance of TaxRegistrationDetail from a dict
tax_registration_detail_from_dict = TaxRegistrationDetail.from_dict(tax_registration_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


