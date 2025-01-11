# CarrierCode

Identifies the carrier that will deliver the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_code_type** | [**CarrierCodeType**](CarrierCodeType.md) |  | [optional] 
**carrier_code_value** | **str** | Value of the carrier code. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.carrier_code import CarrierCode

# TODO update the JSON string below
json = "{}"
# create an instance of CarrierCode from a JSON string
carrier_code_instance = CarrierCode.from_json(json)
# print the JSON string representation of the object
print(CarrierCode.to_json())

# convert the object into a dict
carrier_code_dict = carrier_code_instance.to_dict()
# create an instance of CarrierCode from a dict
carrier_code_from_dict = CarrierCode.from_dict(carrier_code_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


