# InboundShipmentSummary

Summary for an AWD inbound shipment containing the shipment ID, which can be used to retrieve the actual shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Timestamp when the shipment was created. | [optional] 
**external_reference_id** | **str** | Optional client-provided reference ID that can be used to correlate this shipment with client resources. For example, to map this shipment to an internal bookkeeping order record. | [optional] 
**order_id** | **str** | The AWD inbound order ID that this inbound shipment belongs to. | 
**shipment_id** | **str** | A unique shipment ID. | 
**shipment_status** | [**InboundShipmentStatus**](InboundShipmentStatus.md) |  | 
**updated_at** | **datetime** | Timestamp when the shipment was updated. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_shipment_summary import InboundShipmentSummary

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentSummary from a JSON string
inbound_shipment_summary_instance = InboundShipmentSummary.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentSummary.to_json())

# convert the object into a dict
inbound_shipment_summary_dict = inbound_shipment_summary_instance.to_dict()
# create an instance of InboundShipmentSummary from a dict
inbound_shipment_summary_from_dict = InboundShipmentSummary.from_dict(inbound_shipment_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


