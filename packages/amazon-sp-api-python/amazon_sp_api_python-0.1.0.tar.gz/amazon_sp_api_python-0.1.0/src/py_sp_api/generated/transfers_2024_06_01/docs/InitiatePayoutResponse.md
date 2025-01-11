# InitiatePayoutResponse

The response schema for the `initiatePayout` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payout_reference_id** | **str** | The financial event group ID for a successfully initiated payout. You can use this ID to track payout information. | 

## Example

```python
from py_sp_api.generated.transfers_2024_06_01.models.initiate_payout_response import InitiatePayoutResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InitiatePayoutResponse from a JSON string
initiate_payout_response_instance = InitiatePayoutResponse.from_json(json)
# print the JSON string representation of the object
print(InitiatePayoutResponse.to_json())

# convert the object into a dict
initiate_payout_response_dict = initiate_payout_response_instance.to_dict()
# create an instance of InitiatePayoutResponse from a dict
initiate_payout_response_from_dict = InitiatePayoutResponse.from_dict(initiate_payout_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


