# InboundPlanSummary

A light-weight inbound plan.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | The time at which the inbound plan was created. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ssZ&#x60;. | 
**inbound_plan_id** | **str** | Identifier of an inbound plan. | 
**last_updated_at** | **datetime** | The time at which the inbound plan was last updated. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ssZ&#x60;. | 
**marketplace_ids** | **List[str]** | A list of marketplace IDs. | 
**name** | **str** | Human-readable name of the inbound plan. | 
**source_address** | [**Address**](Address.md) |  | 
**status** | **str** | The current status of the inbound plan. Possible values: &#x60;ACTIVE&#x60;, &#x60;VOIDED&#x60;, &#x60;SHIPPED&#x60;, &#x60;ERRORED&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.inbound_plan_summary import InboundPlanSummary

# TODO update the JSON string below
json = "{}"
# create an instance of InboundPlanSummary from a JSON string
inbound_plan_summary_instance = InboundPlanSummary.from_json(json)
# print the JSON string representation of the object
print(InboundPlanSummary.to_json())

# convert the object into a dict
inbound_plan_summary_dict = inbound_plan_summary_instance.to_dict()
# create an instance of InboundPlanSummary from a dict
inbound_plan_summary_from_dict = InboundPlanSummary.from_dict(inbound_plan_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


