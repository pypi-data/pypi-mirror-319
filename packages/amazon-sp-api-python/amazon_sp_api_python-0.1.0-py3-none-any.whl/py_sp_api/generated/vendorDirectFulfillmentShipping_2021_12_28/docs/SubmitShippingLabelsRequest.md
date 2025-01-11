# SubmitShippingLabelsRequest

The request schema for the `submitShippingLabelRequest` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_label_requests** | [**List[ShippingLabelRequest]**](ShippingLabelRequest.md) | An array of shipping label requests to be processed. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.submit_shipping_labels_request import SubmitShippingLabelsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShippingLabelsRequest from a JSON string
submit_shipping_labels_request_instance = SubmitShippingLabelsRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitShippingLabelsRequest.to_json())

# convert the object into a dict
submit_shipping_labels_request_dict = submit_shipping_labels_request_instance.to_dict()
# create an instance of SubmitShippingLabelsRequest from a dict
submit_shipping_labels_request_from_dict = SubmitShippingLabelsRequest.from_dict(submit_shipping_labels_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


