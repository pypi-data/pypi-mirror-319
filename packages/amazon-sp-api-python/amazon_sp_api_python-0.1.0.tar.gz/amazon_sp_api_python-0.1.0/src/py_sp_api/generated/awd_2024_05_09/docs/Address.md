# Address

Shipping address that represents the origin or destination location.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address_line1** | **str** | First line of the address text. | 
**address_line2** | **str** | Optional second line of the address text. | [optional] 
**address_line3** | **str** | Optional third line of the address text. | [optional] 
**city** | **str** | Optional city where this address is located. | [optional] 
**country_code** | **str** | Two-digit, ISO 3166-1 alpha-2 formatted country code where this address is located. | 
**county** | **str** | Optional county where this address is located. | [optional] 
**district** | **str** | Optional district where this address is located. | [optional] 
**name** | **str** | Name of the person, business, or institution at this address. | 
**phone_number** | **str** | Optional E.164-formatted phone number for an available contact at this address. | [optional] 
**postal_code** | **str** | Optional postal code where this address is located. | [optional] 
**state_or_region** | **str** | State or region where this address is located. Note that this is contextual to the specified country code. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.address import Address

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


