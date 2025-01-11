# InboundShipmentItem

Item information for an inbound shipment. Submitted with a call to the createInboundShipment or updateInboundShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | A shipment identifier originally returned by the createInboundShipmentPlan operation. | [optional] 
**seller_sku** | **str** | The seller SKU of the item. | 
**fulfillment_network_sku** | **str** | Amazon&#39;s fulfillment network SKU of the item. | [optional] 
**quantity_shipped** | **int** | The item quantity. | 
**quantity_received** | **int** | The item quantity. | [optional] 
**quantity_in_case** | **int** | The item quantity. | [optional] 
**release_date** | **date** | Type containing date in string format | [optional] 
**prep_details_list** | [**List[PrepDetails]**](PrepDetails.md) | A list of preparation instructions and who is responsible for that preparation. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_item import InboundShipmentItem

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentItem from a JSON string
inbound_shipment_item_instance = InboundShipmentItem.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentItem.to_json())

# convert the object into a dict
inbound_shipment_item_dict = inbound_shipment_item_instance.to_dict()
# create an instance of InboundShipmentItem from a dict
inbound_shipment_item_from_dict = InboundShipmentItem.from_dict(inbound_shipment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


