# Address

A physical address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person, business or institution at that address. | 
**address_line1** | **str** | First line of street address. | 
**address_line2** | **str** | Additional address information, if required. | [optional] 
**address_line3** | **str** | Additional address information, if required. | [optional] 
**city** | **str** | The city where the person, business or institution is located. | [optional] 
**county** | **str** | The county where person, business or institution is located. | [optional] 
**district** | **str** | The district where person, business or institution is located. | [optional] 
**state_or_region** | **str** | The state or region where person, business or institution is located. | [optional] 
**postal_or_zip_code** | **str** | The postal or zip code of that address. It contains a series of letters or digits or both, sometimes including spaces or punctuation. | [optional] 
**country_code** | **str** | The two digit country code. In ISO 3166-1 alpha-2 format. | 
**phone** | **str** | The phone number of the person, business or institution located at that address. | [optional] 

## Example

```python
from py_sp_api.generated.vendorInvoices.models.address import Address

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


