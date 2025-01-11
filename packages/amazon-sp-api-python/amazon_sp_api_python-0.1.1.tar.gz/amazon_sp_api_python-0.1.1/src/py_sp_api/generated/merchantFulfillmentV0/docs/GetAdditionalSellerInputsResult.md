# GetAdditionalSellerInputsResult

The payload for the `getAdditionalSellerInputs` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_level_fields** | [**List[AdditionalInputs]**](AdditionalInputs.md) | A list of additional inputs. | [optional] 
**item_level_fields_list** | [**List[ItemLevelFields]**](ItemLevelFields.md) | A list of item level fields. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_additional_seller_inputs_result import GetAdditionalSellerInputsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetAdditionalSellerInputsResult from a JSON string
get_additional_seller_inputs_result_instance = GetAdditionalSellerInputsResult.from_json(json)
# print the JSON string representation of the object
print(GetAdditionalSellerInputsResult.to_json())

# convert the object into a dict
get_additional_seller_inputs_result_dict = get_additional_seller_inputs_result_instance.to_dict()
# create an instance of GetAdditionalSellerInputsResult from a dict
get_additional_seller_inputs_result_from_dict = GetAdditionalSellerInputsResult.from_dict(get_additional_seller_inputs_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


