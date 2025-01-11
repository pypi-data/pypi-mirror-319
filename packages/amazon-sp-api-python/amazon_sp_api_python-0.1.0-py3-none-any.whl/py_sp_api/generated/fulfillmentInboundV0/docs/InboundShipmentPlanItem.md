# InboundShipmentPlanItem

Item information used to create an inbound shipment. Returned by the createInboundShipmentPlan operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**fulfillment_network_sku** | **str** | Amazon&#39;s fulfillment network SKU of the item. | 
**quantity** | **int** | The item quantity. | 
**prep_details_list** | [**List[PrepDetails]**](PrepDetails.md) | A list of preparation instructions and who is responsible for that preparation. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_plan_item import InboundShipmentPlanItem

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentPlanItem from a JSON string
inbound_shipment_plan_item_instance = InboundShipmentPlanItem.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentPlanItem.to_json())

# convert the object into a dict
inbound_shipment_plan_item_dict = inbound_shipment_plan_item_instance.to_dict()
# create an instance of InboundShipmentPlanItem from a dict
inbound_shipment_plan_item_from_dict = InboundShipmentPlanItem.from_dict(inbound_shipment_plan_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


