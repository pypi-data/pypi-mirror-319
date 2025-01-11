# SubmitAcknowledgementRequest

The request schema for the submitAcknowledgement operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_acknowledgements** | [**List[OrderAcknowledgementItem]**](OrderAcknowledgementItem.md) | A list of one or more purchase orders. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.submit_acknowledgement_request import SubmitAcknowledgementRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitAcknowledgementRequest from a JSON string
submit_acknowledgement_request_instance = SubmitAcknowledgementRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitAcknowledgementRequest.to_json())

# convert the object into a dict
submit_acknowledgement_request_dict = submit_acknowledgement_request_instance.to_dict()
# create an instance of SubmitAcknowledgementRequest from a dict
submit_acknowledgement_request_from_dict = SubmitAcknowledgementRequest.from_dict(submit_acknowledgement_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


