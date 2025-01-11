# ListInboundPlansResponse

The `listInboundPlans` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_plans** | [**List[InboundPlanSummary]**](InboundPlanSummary.md) | A list of inbound plans with minimal information. | [optional] 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_inbound_plans_response import ListInboundPlansResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListInboundPlansResponse from a JSON string
list_inbound_plans_response_instance = ListInboundPlansResponse.from_json(json)
# print the JSON string representation of the object
print(ListInboundPlansResponse.to_json())

# convert the object into a dict
list_inbound_plans_response_dict = list_inbound_plans_response_instance.to_dict()
# create an instance of ListInboundPlansResponse from a dict
list_inbound_plans_response_from_dict = ListInboundPlansResponse.from_dict(list_inbound_plans_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


