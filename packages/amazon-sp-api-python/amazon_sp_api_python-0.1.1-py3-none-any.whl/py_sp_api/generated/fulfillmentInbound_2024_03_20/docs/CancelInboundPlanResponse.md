# CancelInboundPlanResponse

The `cancelInboundPlan` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.cancel_inbound_plan_response import CancelInboundPlanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelInboundPlanResponse from a JSON string
cancel_inbound_plan_response_instance = CancelInboundPlanResponse.from_json(json)
# print the JSON string representation of the object
print(CancelInboundPlanResponse.to_json())

# convert the object into a dict
cancel_inbound_plan_response_dict = cancel_inbound_plan_response_instance.to_dict()
# create an instance of CancelInboundPlanResponse from a dict
cancel_inbound_plan_response_from_dict = CancelInboundPlanResponse.from_dict(cancel_inbound_plan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


