# CreateInboundPlanResponse

The `createInboundPlan` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_plan_id** | **str** | Identifier of an inbound plan. | 
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.create_inbound_plan_response import CreateInboundPlanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInboundPlanResponse from a JSON string
create_inbound_plan_response_instance = CreateInboundPlanResponse.from_json(json)
# print the JSON string representation of the object
print(CreateInboundPlanResponse.to_json())

# convert the object into a dict
create_inbound_plan_response_dict = create_inbound_plan_response_instance.to_dict()
# create an instance of CreateInboundPlanResponse from a dict
create_inbound_plan_response_from_dict = CreateInboundPlanResponse.from_dict(create_inbound_plan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


