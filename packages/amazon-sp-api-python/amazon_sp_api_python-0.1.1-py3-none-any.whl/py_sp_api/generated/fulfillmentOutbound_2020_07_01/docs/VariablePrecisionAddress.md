# VariablePrecisionAddress

A physical address with varying degrees of precision. A more precise address can provide more accurate results than country code and postal code alone.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address_line1** | **str** | The first line of the address. | [optional] 
**address_line2** | **str** | Additional address information, if required. | [optional] 
**address_line3** | **str** | Additional address information, if required. | [optional] 
**city** | **str** | The city where the person, business, or institution is located. This property should not be used in Japan. | [optional] 
**district_or_county** | **str** | The district or county where the person, business, or institution is located. | [optional] 
**state_or_region** | **str** | The state or region where the person, business or institution is located. | [optional] 
**postal_code** | **str** | The postal code of the address. | 
**country_code** | **str** | The two digit country code. In ISO 3166-1 alpha-2 format. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.variable_precision_address import VariablePrecisionAddress

# TODO update the JSON string below
json = "{}"
# create an instance of VariablePrecisionAddress from a JSON string
variable_precision_address_instance = VariablePrecisionAddress.from_json(json)
# print the JSON string representation of the object
print(VariablePrecisionAddress.to_json())

# convert the object into a dict
variable_precision_address_dict = variable_precision_address_instance.to_dict()
# create an instance of VariablePrecisionAddress from a dict
variable_precision_address_from_dict = VariablePrecisionAddress.from_dict(variable_precision_address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


