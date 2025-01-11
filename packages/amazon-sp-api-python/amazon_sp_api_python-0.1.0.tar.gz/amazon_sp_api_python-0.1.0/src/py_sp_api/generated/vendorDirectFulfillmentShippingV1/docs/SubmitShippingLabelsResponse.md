# SubmitShippingLabelsResponse

The response schema for the submitShippingLabelRequest operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionReference**](TransactionReference.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipping_labels_response import SubmitShippingLabelsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShippingLabelsResponse from a JSON string
submit_shipping_labels_response_instance = SubmitShippingLabelsResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitShippingLabelsResponse.to_json())

# convert the object into a dict
submit_shipping_labels_response_dict = submit_shipping_labels_response_instance.to_dict()
# create an instance of SubmitShippingLabelsResponse from a dict
submit_shipping_labels_response_from_dict = SubmitShippingLabelsResponse.from_dict(submit_shipping_labels_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


