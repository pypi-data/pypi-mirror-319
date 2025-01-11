# UpdateInboundPlanNameRequest

The `updateInboundPlanName` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A human-readable name to update the inbound plan name to. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_inbound_plan_name_request import UpdateInboundPlanNameRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateInboundPlanNameRequest from a JSON string
update_inbound_plan_name_request_instance = UpdateInboundPlanNameRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateInboundPlanNameRequest.to_json())

# convert the object into a dict
update_inbound_plan_name_request_dict = update_inbound_plan_name_request_instance.to_dict()
# create an instance of UpdateInboundPlanNameRequest from a dict
update_inbound_plan_name_request_from_dict = UpdateInboundPlanNameRequest.from_dict(update_inbound_plan_name_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


