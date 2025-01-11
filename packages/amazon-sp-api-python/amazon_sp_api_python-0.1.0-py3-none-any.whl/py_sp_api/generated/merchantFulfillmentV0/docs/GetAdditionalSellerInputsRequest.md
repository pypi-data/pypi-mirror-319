# GetAdditionalSellerInputsRequest

Request schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_service_id** | **str** | An Amazon-defined shipping service identifier. | 
**ship_from_address** | [**Address**](Address.md) |  | 
**order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_additional_seller_inputs_request import GetAdditionalSellerInputsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetAdditionalSellerInputsRequest from a JSON string
get_additional_seller_inputs_request_instance = GetAdditionalSellerInputsRequest.from_json(json)
# print the JSON string representation of the object
print(GetAdditionalSellerInputsRequest.to_json())

# convert the object into a dict
get_additional_seller_inputs_request_dict = get_additional_seller_inputs_request_instance.to_dict()
# create an instance of GetAdditionalSellerInputsRequest from a dict
get_additional_seller_inputs_request_from_dict = GetAdditionalSellerInputsRequest.from_dict(get_additional_seller_inputs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


