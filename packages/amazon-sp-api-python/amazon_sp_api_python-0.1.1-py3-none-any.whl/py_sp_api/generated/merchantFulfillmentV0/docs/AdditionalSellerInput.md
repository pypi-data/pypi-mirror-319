# AdditionalSellerInput

Additional information required to purchase shipping.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | The data type of the additional information. | [optional] 
**value_as_string** | **str** | The value when the data type is string. | [optional] 
**value_as_boolean** | **bool** | The value when the data type is boolean. | [optional] 
**value_as_integer** | **int** | The value when the data type is integer. | [optional] 
**value_as_timestamp** | **datetime** | Date-time formatted timestamp. | [optional] 
**value_as_address** | [**Address**](Address.md) |  | [optional] 
**value_as_weight** | [**Weight**](Weight.md) |  | [optional] 
**value_as_dimension** | [**Length**](Length.md) |  | [optional] 
**value_as_currency** | [**CurrencyAmount**](CurrencyAmount.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.additional_seller_input import AdditionalSellerInput

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalSellerInput from a JSON string
additional_seller_input_instance = AdditionalSellerInput.from_json(json)
# print the JSON string representation of the object
print(AdditionalSellerInput.to_json())

# convert the object into a dict
additional_seller_input_dict = additional_seller_input_instance.to_dict()
# create an instance of AdditionalSellerInput from a dict
additional_seller_input_from_dict = AdditionalSellerInput.from_dict(additional_seller_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


