# CreateInboundShipmentPlanResponse

The response schema for the createInboundShipmentPlan operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateInboundShipmentPlanResult**](CreateInboundShipmentPlanResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.create_inbound_shipment_plan_response import CreateInboundShipmentPlanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInboundShipmentPlanResponse from a JSON string
create_inbound_shipment_plan_response_instance = CreateInboundShipmentPlanResponse.from_json(json)
# print the JSON string representation of the object
print(CreateInboundShipmentPlanResponse.to_json())

# convert the object into a dict
create_inbound_shipment_plan_response_dict = create_inbound_shipment_plan_response_instance.to_dict()
# create an instance of CreateInboundShipmentPlanResponse from a dict
create_inbound_shipment_plan_response_from_dict = CreateInboundShipmentPlanResponse.from_dict(create_inbound_shipment_plan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


