# Address

Specific details to identify a place.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the individual or business. | 
**address_line1** | **str** | The street address information. | 
**address_line2** | **str** | Additional street address information, if required. | [optional] 
**district_or_county** | **str** | The district or county. | [optional] 
**city** | **str** | The city. | 
**state_or_province_code** | **str** | The state or province code.  If state or province codes are used in your marketplace, it is recommended that you include one with your request. This helps Amazon to select the most appropriate Amazon fulfillment center for your inbound shipment plan. | 
**country_code** | **str** | The country code in two-character ISO 3166-1 alpha-2 format. | 
**postal_code** | **str** | The postal code.  If postal codes are used in your marketplace, we recommended that you include one with your request. This helps Amazon select the most appropriate Amazon fulfillment center for the inbound shipment plan. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.address import Address

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


