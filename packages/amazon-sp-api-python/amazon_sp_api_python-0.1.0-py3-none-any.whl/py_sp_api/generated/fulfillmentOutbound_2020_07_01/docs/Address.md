# Address

A physical address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the person, business or institution at the address. | 
**address_line1** | **str** | The first line of the address. | 
**address_line2** | **str** | Additional address information, if required. | [optional] 
**address_line3** | **str** | Additional address information, if required. | [optional] 
**city** | **str** | The city where the person, business, or institution is located. This property is required in all countries except Japan. It should not be used in Japan. | [optional] 
**district_or_county** | **str** | The district or county where the person, business, or institution is located. | [optional] 
**state_or_region** | **str** | The state or region where the person, business or institution is located. | 
**postal_code** | **str** | The postal code of the address. | 
**country_code** | **str** | The two digit country code. In ISO 3166-1 alpha-2 format. | 
**phone** | **str** | The phone number of the person, business, or institution located at the address. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.address import Address

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


