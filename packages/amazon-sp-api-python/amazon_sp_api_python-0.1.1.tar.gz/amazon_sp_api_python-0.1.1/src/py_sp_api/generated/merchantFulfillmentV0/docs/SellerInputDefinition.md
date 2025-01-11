# SellerInputDefinition

Specifies characteristics that apply to a seller input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_required** | **bool** | When true, the additional input field is required. | 
**data_type** | **str** | The data type of the additional input field. | 
**constraints** | [**List[Constraint]**](Constraint.md) | List of constraints. | 
**input_display_text** | **str** | The display text for the additional input field. | 
**input_target** | [**InputTargetType**](InputTargetType.md) |  | [optional] 
**stored_value** | [**AdditionalSellerInput**](AdditionalSellerInput.md) |  | 
**restricted_set_values** | **List[str]** | The set of fixed values in an additional seller input. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.seller_input_definition import SellerInputDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of SellerInputDefinition from a JSON string
seller_input_definition_instance = SellerInputDefinition.from_json(json)
# print the JSON string representation of the object
print(SellerInputDefinition.to_json())

# convert the object into a dict
seller_input_definition_dict = seller_input_definition_instance.to_dict()
# create an instance of SellerInputDefinition from a dict
seller_input_definition_from_dict = SellerInputDefinition.from_dict(seller_input_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


