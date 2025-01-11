# Address

The address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person, business or institution at that address. | 
**address_line1** | **str** | First line of that address. | 
**address_line2** | **str** | Additional address information, if required. | [optional] 
**address_line3** | **str** | Additional address information, if required. | [optional] 
**state_or_region** | **str** | The state or region where the person, business or institution is located. | 
**city** | **str** | The city where the person, business or institution is located. | 
**country_code** | **str** | The two digit country code. In ISO 3166-1 alpha-2 format. | 
**postal_code** | **str** | The postal code of that address. It contains a series of letters or digits or both, sometimes including spaces or punctuation. | 
**email** | **str** | The email address of the contact associated with the address. | [optional] 
**copy_emails** | **List[str]** | The email cc addresses of the contact associated with the address. | [optional] 
**phone_number** | **str** | The phone number of the person, business or institution located at that address. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.address import Address

# TODO update the JSON string below
json = "{}"
# create an instance of Address from a JSON string
address_instance = Address.from_json(json)
# print the JSON string representation of the object
print(Address.to_json())

# convert the object into a dict
address_dict = address_instance.to_dict()
# create an instance of Address from a dict
address_from_dict = Address.from_dict(address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


