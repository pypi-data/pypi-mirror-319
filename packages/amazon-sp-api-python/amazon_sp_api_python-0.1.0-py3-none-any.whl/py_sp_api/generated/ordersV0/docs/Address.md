# Address

The shipping address for the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name. | 
**company_name** | **str** | The company name of the recipient.  **Note**: This attribute is only available for shipping address. | [optional] 
**address_line1** | **str** | The street address. | [optional] 
**address_line2** | **str** | Additional street address information, if required. | [optional] 
**address_line3** | **str** | Additional street address information, if required. | [optional] 
**city** | **str** | The city. | [optional] 
**county** | **str** | The county. | [optional] 
**district** | **str** | The district. | [optional] 
**state_or_region** | **str** | The state or region. | [optional] 
**municipality** | **str** | The municipality. | [optional] 
**postal_code** | **str** | The postal code. | [optional] 
**country_code** | **str** | The country code. A two-character country code, in ISO 3166-1 alpha-2 format. | [optional] 
**phone** | **str** | The phone number of the buyer.  **Note**:  1. This attribute is only available for shipping address. 2. In some cases, the buyer phone number is suppressed:  a. Phone is suppressed for all &#x60;AFN&#x60; (fulfilled by Amazon) orders. b. Phone is suppressed for the shipped &#x60;MFN&#x60; (fulfilled by seller) order when the current date is past the Latest Delivery Date. | [optional] 
**extended_fields** | [**AddressExtendedFields**](AddressExtendedFields.md) |  | [optional] 
**address_type** | **str** | The address type of the shipping address. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.address import Address

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


