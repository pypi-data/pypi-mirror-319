# CreateInboundShipmentPlanResult

Result for the create inbound shipment operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_shipment_plans** | [**List[InboundShipmentPlan]**](InboundShipmentPlan.md) | A list of inbound shipment plan information | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.create_inbound_shipment_plan_result import CreateInboundShipmentPlanResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInboundShipmentPlanResult from a JSON string
create_inbound_shipment_plan_result_instance = CreateInboundShipmentPlanResult.from_json(json)
# print the JSON string representation of the object
print(CreateInboundShipmentPlanResult.to_json())

# convert the object into a dict
create_inbound_shipment_plan_result_dict = create_inbound_shipment_plan_result_instance.to_dict()
# create an instance of CreateInboundShipmentPlanResult from a dict
create_inbound_shipment_plan_result_from_dict = CreateInboundShipmentPlanResult.from_dict(create_inbound_shipment_plan_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


