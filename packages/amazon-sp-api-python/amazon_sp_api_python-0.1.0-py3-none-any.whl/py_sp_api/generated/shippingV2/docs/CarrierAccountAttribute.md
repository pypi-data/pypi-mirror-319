# CarrierAccountAttribute

Attribute Properties required by carrier

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_name** | **str** | Attribute Name . | [optional] 
**property_group** | **str** | Property Group. | [optional] 
**value** | **str** | Value . | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.carrier_account_attribute import CarrierAccountAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of CarrierAccountAttribute from a JSON string
carrier_account_attribute_instance = CarrierAccountAttribute.from_json(json)
# print the JSON string representation of the object
print(CarrierAccountAttribute.to_json())

# convert the object into a dict
carrier_account_attribute_dict = carrier_account_attribute_instance.to_dict()
# create an instance of CarrierAccountAttribute from a dict
carrier_account_attribute_from_dict = CarrierAccountAttribute.from_dict(carrier_account_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


