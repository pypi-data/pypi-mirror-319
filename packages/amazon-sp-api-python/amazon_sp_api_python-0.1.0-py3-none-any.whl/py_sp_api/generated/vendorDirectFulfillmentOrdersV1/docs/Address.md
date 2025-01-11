# Address

Address of the party.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person, business or institution at that address. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | 
**attention** | **str** | The attention name of the person at that address. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**address_line1** | **str** | First line of the address. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | 
**address_line2** | **str** | Additional address information, if required. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**address_line3** | **str** | Additional address information, if required. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**city** | **str** | The city where the person, business or institution is located. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**county** | **str** | The county where person, business or institution is located. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**district** | **str** | The district where person, business or institution is located. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 
**state_or_region** | **str** | The state or region where person, business or institution is located. | 
**postal_code** | **str** | The postal code of that address. It conatins a series of letters or digits or both, sometimes including spaces or punctuation. | [optional] 
**country_code** | **str** | The two digit country code. In ISO 3166-1 alpha-2 format. | 
**phone** | **str** | The phone number of the person, business or institution located at that address. For Amazon label only vendors, this field will have the value &#x60;xxxxx&#x60; within the object &#x60;shipToParty&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.address import Address

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


