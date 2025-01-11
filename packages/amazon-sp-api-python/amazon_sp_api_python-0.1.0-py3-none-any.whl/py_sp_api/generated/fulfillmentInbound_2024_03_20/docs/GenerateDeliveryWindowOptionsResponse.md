# GenerateDeliveryWindowOptionsResponse

The `generateDeliveryWindowOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_delivery_window_options_response import GenerateDeliveryWindowOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateDeliveryWindowOptionsResponse from a JSON string
generate_delivery_window_options_response_instance = GenerateDeliveryWindowOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateDeliveryWindowOptionsResponse.to_json())

# convert the object into a dict
generate_delivery_window_options_response_dict = generate_delivery_window_options_response_instance.to_dict()
# create an instance of GenerateDeliveryWindowOptionsResponse from a dict
generate_delivery_window_options_response_from_dict = GenerateDeliveryWindowOptionsResponse.from_dict(generate_delivery_window_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


