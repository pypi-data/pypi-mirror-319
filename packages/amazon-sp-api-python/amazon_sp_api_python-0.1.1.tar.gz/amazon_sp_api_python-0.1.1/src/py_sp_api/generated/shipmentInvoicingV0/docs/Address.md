# Address

The shipping address details of the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name. | [optional] 
**address_line1** | **str** | The street address. | [optional] 
**address_line2** | **str** | Additional street address information, if required. | [optional] 
**address_line3** | **str** | Additional street address information, if required. | [optional] 
**city** | **str** | The city. | [optional] 
**county** | **str** | The county. | [optional] 
**district** | **str** | The district. | [optional] 
**state_or_region** | **str** | The state or region. | [optional] 
**postal_code** | **str** | The postal code. | [optional] 
**country_code** | **str** | The country code. | [optional] 
**phone** | **str** | The phone number. | [optional] 
**address_type** | [**AddressTypeEnum**](AddressTypeEnum.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.address import Address

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


