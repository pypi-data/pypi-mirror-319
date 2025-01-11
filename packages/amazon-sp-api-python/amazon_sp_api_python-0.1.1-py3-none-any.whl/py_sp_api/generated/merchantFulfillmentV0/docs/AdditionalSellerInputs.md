# AdditionalSellerInputs

An additional set of seller inputs required to purchase shipping.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_input_field_name** | **str** | The name of the additional input field. | 
**additional_seller_input** | [**AdditionalSellerInput**](AdditionalSellerInput.md) |  | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.additional_seller_inputs import AdditionalSellerInputs

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalSellerInputs from a JSON string
additional_seller_inputs_instance = AdditionalSellerInputs.from_json(json)
# print the JSON string representation of the object
print(AdditionalSellerInputs.to_json())

# convert the object into a dict
additional_seller_inputs_dict = additional_seller_inputs_instance.to_dict()
# create an instance of AdditionalSellerInputs from a dict
additional_seller_inputs_from_dict = AdditionalSellerInputs.from_dict(additional_seller_inputs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


