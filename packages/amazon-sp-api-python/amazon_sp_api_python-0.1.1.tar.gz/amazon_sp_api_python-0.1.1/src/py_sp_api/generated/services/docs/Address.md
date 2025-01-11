# Address

The shipping address for the service job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person, business, or institution. | 
**address_line1** | **str** | The first line of the address. | 
**address_line2** | **str** | Additional address information, if required. | [optional] 
**address_line3** | **str** | Additional address information, if required. | [optional] 
**city** | **str** | The city. | [optional] 
**county** | **str** | The county. | [optional] 
**district** | **str** | The district. | [optional] 
**state_or_region** | **str** | The state or region. | [optional] 
**postal_code** | **str** | The postal code. This can contain letters, digits, spaces, and/or punctuation. | [optional] 
**country_code** | **str** | The two digit country code, in ISO 3166-1 alpha-2 format. | [optional] 
**phone** | **str** | The phone number. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.address import Address

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


