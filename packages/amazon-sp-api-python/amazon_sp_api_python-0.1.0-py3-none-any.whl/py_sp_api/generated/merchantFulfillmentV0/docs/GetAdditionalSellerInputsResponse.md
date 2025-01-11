# GetAdditionalSellerInputsResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetAdditionalSellerInputsResult**](GetAdditionalSellerInputsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_additional_seller_inputs_response import GetAdditionalSellerInputsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetAdditionalSellerInputsResponse from a JSON string
get_additional_seller_inputs_response_instance = GetAdditionalSellerInputsResponse.from_json(json)
# print the JSON string representation of the object
print(GetAdditionalSellerInputsResponse.to_json())

# convert the object into a dict
get_additional_seller_inputs_response_dict = get_additional_seller_inputs_response_instance.to_dict()
# create an instance of GetAdditionalSellerInputsResponse from a dict
get_additional_seller_inputs_response_from_dict = GetAdditionalSellerInputsResponse.from_dict(get_additional_seller_inputs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


