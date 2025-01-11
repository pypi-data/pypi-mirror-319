# Address

The postal address information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the addressee, or business name. | 
**address_line1** | **str** | The street address information. | 
**address_line2** | **str** | Additional street address information. | [optional] 
**address_line3** | **str** | Additional street address information. | [optional] 
**district_or_county** | **str** | The district or county. | [optional] 
**email** | **str** | The email address. | 
**city** | **str** | The city. | 
**state_or_province_code** | **str** | The state or province code. This is a required field in Canada, US, and UK marketplaces, and for shipments that originate in China. | [optional] 
**postal_code** | **str** | The zip code or postal code. | 
**country_code** | **str** | The two-letter country code in [ISO 3166-1 alpha-2](https://www.iban.com/country-codes) format. | 
**phone** | **str** | The phone number. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.address import Address

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


