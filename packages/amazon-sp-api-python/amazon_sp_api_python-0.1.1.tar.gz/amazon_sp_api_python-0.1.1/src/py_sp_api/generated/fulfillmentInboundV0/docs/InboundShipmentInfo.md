# InboundShipmentInfo

Information about the seller's inbound shipments. Returned by the listInboundShipments operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The shipment identifier submitted in the request. | [optional] 
**shipment_name** | **str** | The name for the inbound shipment. | [optional] 
**ship_from_address** | [**Address**](Address.md) |  | 
**destination_fulfillment_center_id** | **str** | An Amazon fulfillment center identifier created by Amazon. | [optional] 
**shipment_status** | [**ShipmentStatus**](ShipmentStatus.md) |  | [optional] 
**label_prep_type** | [**LabelPrepType**](LabelPrepType.md) |  | [optional] 
**are_cases_required** | **bool** | Indicates whether or not an inbound shipment contains case-packed boxes. When AreCasesRequired &#x3D; true for an inbound shipment, all items in the inbound shipment must be case packed. | 
**confirmed_need_by_date** | **date** | Type containing date in string format | [optional] 
**box_contents_source** | [**BoxContentsSource**](BoxContentsSource.md) |  | [optional] 
**estimated_box_contents_fee** | [**BoxContentsFeeDetails**](BoxContentsFeeDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_info import InboundShipmentInfo

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentInfo from a JSON string
inbound_shipment_info_instance = InboundShipmentInfo.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentInfo.to_json())

# convert the object into a dict
inbound_shipment_info_dict = inbound_shipment_info_instance.to_dict()
# create an instance of InboundShipmentInfo from a dict
inbound_shipment_info_from_dict = InboundShipmentInfo.from_dict(inbound_shipment_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


