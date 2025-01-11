# CarrierAccountInput

Info About CarrierAccountInput

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description_localization_key** | **str** | descriptionLocalizationKey value . | [optional] 
**name** | **str** | name value . | [optional] 
**group_name** | **str** | groupName value . | [optional] 
**input_type** | [**InputType**](InputType.md) |  | [optional] 
**is_mandatory** | **bool** | mandatory or not  value . | [optional] 
**is_confidential** | **bool** | is value is Confidential . | [optional] 
**is_hidden** | **bool** | is value is hidden . | [optional] 
**validation_metadata** | [**List[ValidationMetadata]**](ValidationMetadata.md) | A list of ValidationMetadata | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.carrier_account_input import CarrierAccountInput

# TODO update the JSON string below
json = "{}"
# create an instance of CarrierAccountInput from a JSON string
carrier_account_input_instance = CarrierAccountInput.from_json(json)
# print the JSON string representation of the object
print(CarrierAccountInput.to_json())

# convert the object into a dict
carrier_account_input_dict = carrier_account_input_instance.to_dict()
# create an instance of CarrierAccountInput from a dict
carrier_account_input_from_dict = CarrierAccountInput.from_dict(carrier_account_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


