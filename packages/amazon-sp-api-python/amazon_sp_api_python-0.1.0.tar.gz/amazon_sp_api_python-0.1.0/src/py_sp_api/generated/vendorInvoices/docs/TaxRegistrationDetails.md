# TaxRegistrationDetails

Tax registration details of the entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_registration_type** | **str** | The tax registration type for the entity. | 
**tax_registration_number** | **str** | The tax registration number for the entity. For example, VAT ID, Consumption Tax ID. | 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.tax_registration_details import TaxRegistrationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TaxRegistrationDetails from a JSON string
tax_registration_details_instance = TaxRegistrationDetails.from_json(json)
# print the JSON string representation of the object
print(TaxRegistrationDetails.to_json())

# convert the object into a dict
tax_registration_details_dict = tax_registration_details_instance.to_dict()
# create an instance of TaxRegistrationDetails from a dict
tax_registration_details_from_dict = TaxRegistrationDetails.from_dict(tax_registration_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


