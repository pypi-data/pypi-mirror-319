# AdditionalInputs

Maps the additional seller input to the definition. The key to the map is the field name.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_input_field_name** | **str** | The field name. | [optional] 
**seller_input_definition** | [**SellerInputDefinition**](SellerInputDefinition.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.additional_inputs import AdditionalInputs

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalInputs from a JSON string
additional_inputs_instance = AdditionalInputs.from_json(json)
# print the JSON string representation of the object
print(AdditionalInputs.to_json())

# convert the object into a dict
additional_inputs_dict = additional_inputs_instance.to_dict()
# create an instance of AdditionalInputs from a dict
additional_inputs_from_dict = AdditionalInputs.from_dict(additional_inputs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


