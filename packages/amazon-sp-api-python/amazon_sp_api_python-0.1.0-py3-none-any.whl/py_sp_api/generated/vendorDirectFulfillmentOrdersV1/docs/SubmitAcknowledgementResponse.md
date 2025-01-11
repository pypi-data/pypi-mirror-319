# SubmitAcknowledgementResponse

The response schema for the submitAcknowledgement operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionId**](TransactionId.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.submit_acknowledgement_response import SubmitAcknowledgementResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitAcknowledgementResponse from a JSON string
submit_acknowledgement_response_instance = SubmitAcknowledgementResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitAcknowledgementResponse.to_json())

# convert the object into a dict
submit_acknowledgement_response_dict = submit_acknowledgement_response_instance.to_dict()
# create an instance of SubmitAcknowledgementResponse from a dict
submit_acknowledgement_response_from_dict = SubmitAcknowledgementResponse.from_dict(submit_acknowledgement_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


