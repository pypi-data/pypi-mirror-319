# AddressInput

Specific details to identify a place.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address_line1** | **str** | Street address information. | 
**address_line2** | **str** | Additional street address information. | [optional] 
**city** | **str** | The city. | 
**company_name** | **str** | The name of the business. | [optional] 
**country_code** | **str** | The country code in two-character ISO 3166-1 alpha-2 format. | 
**email** | **str** | The email address. | [optional] 
**name** | **str** | The name of the individual who is the primary contact. | 
**phone_number** | **str** | The phone number. | 
**postal_code** | **str** | The postal code. | 
**state_or_province_code** | **str** | The state or province code. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.address_input import AddressInput

# TODO update the JSON string below
json = "{}"
# create an instance of AddressInput from a JSON string
address_input_instance = AddressInput.from_json(json)
# print the JSON string representation of the object
print(AddressInput.to_json())

# convert the object into a dict
address_input_dict = address_input_instance.to_dict()
# create an instance of AddressInput from a dict
address_input_from_dict = AddressInput.from_dict(address_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


