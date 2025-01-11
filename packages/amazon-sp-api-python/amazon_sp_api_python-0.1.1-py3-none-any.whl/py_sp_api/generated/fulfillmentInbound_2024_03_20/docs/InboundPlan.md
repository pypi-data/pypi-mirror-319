# InboundPlan

Inbound plan containing details of the inbound workflow.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | The time at which the inbound plan was created. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime with pattern &#x60;yyyy-MM-ddTHH:mm:ssZ&#x60;. | 
**inbound_plan_id** | **str** | Identifier of an inbound plan. | 
**last_updated_at** | **datetime** | The time at which the inbound plan was last updated. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ssZ&#x60;. | 
**marketplace_ids** | **List[str]** | A list of marketplace IDs. | 
**name** | **str** | Human-readable name of the inbound plan. | 
**packing_options** | [**List[PackingOptionSummary]**](PackingOptionSummary.md) | Packing options for the inbound plan. This property will be populated when it has been generated via the corresponding operation. If there is a chosen placement option, only packing options for that placement option will be returned. If there are confirmed shipments, only packing options for those shipments will be returned. Query the packing option for more details. | [optional] 
**placement_options** | [**List[PlacementOptionSummary]**](PlacementOptionSummary.md) | Placement options for the inbound plan. This property will be populated when it has been generated via the corresponding operation. If there is a chosen placement option, that will be the only returned option. Query the placement option for more details. | [optional] 
**shipments** | [**List[ShipmentSummary]**](ShipmentSummary.md) | A list of shipment IDs for the inbound plan. This property is populated when it has been generated with the &#x60;confirmPlacementOptions&#x60; operation. Only shipments from the chosen placement option are returned. Query the shipment for more details. | [optional] 
**source_address** | [**Address**](Address.md) |  | 
**status** | **str** | Current status of the inbound plan. Possible values: &#x60;ACTIVE&#x60;, &#x60;VOIDED&#x60;, &#x60;SHIPPED&#x60;, &#x60;ERRORED&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.inbound_plan import InboundPlan

# TODO update the JSON string below
json = "{}"
# create an instance of InboundPlan from a JSON string
inbound_plan_instance = InboundPlan.from_json(json)
# print the JSON string representation of the object
print(InboundPlan.to_json())

# convert the object into a dict
inbound_plan_dict = inbound_plan_instance.to_dict()
# create an instance of InboundPlan from a dict
inbound_plan_from_dict = InboundPlan.from_dict(inbound_plan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


