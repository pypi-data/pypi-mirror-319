# InboundShipmentPlanRequestItem

Item information for creating an inbound shipment plan. Submitted with a call to the createInboundShipmentPlan operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | 
**condition** | [**Condition**](Condition.md) |  | 
**quantity** | **int** | The item quantity. | 
**quantity_in_case** | **int** | The item quantity. | [optional] 
**prep_details_list** | [**List[PrepDetails]**](PrepDetails.md) | A list of preparation instructions and who is responsible for that preparation. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_plan_request_item import InboundShipmentPlanRequestItem

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentPlanRequestItem from a JSON string
inbound_shipment_plan_request_item_instance = InboundShipmentPlanRequestItem.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentPlanRequestItem.to_json())

# convert the object into a dict
inbound_shipment_plan_request_item_dict = inbound_shipment_plan_request_item_instance.to_dict()
# create an instance of InboundShipmentPlanRequestItem from a dict
inbound_shipment_plan_request_item_from_dict = InboundShipmentPlanRequestItem.from_dict(inbound_shipment_plan_request_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


