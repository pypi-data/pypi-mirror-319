# InboundShipmentPlan

Inbound shipment information used to create an inbound shipment. Returned by the createInboundShipmentPlan operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | A shipment identifier originally returned by the createInboundShipmentPlan operation. | 
**destination_fulfillment_center_id** | **str** | An Amazon fulfillment center identifier created by Amazon. | 
**ship_to_address** | [**Address**](Address.md) |  | 
**label_prep_type** | [**LabelPrepType**](LabelPrepType.md) |  | 
**items** | [**List[InboundShipmentPlanItem]**](InboundShipmentPlanItem.md) | A list of inbound shipment plan item information. | 
**estimated_box_contents_fee** | [**BoxContentsFeeDetails**](BoxContentsFeeDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_plan import InboundShipmentPlan

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentPlan from a JSON string
inbound_shipment_plan_instance = InboundShipmentPlan.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentPlan.to_json())

# convert the object into a dict
inbound_shipment_plan_dict = inbound_shipment_plan_instance.to_dict()
# create an instance of InboundShipmentPlan from a dict
inbound_shipment_plan_from_dict = InboundShipmentPlan.from_dict(inbound_shipment_plan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


