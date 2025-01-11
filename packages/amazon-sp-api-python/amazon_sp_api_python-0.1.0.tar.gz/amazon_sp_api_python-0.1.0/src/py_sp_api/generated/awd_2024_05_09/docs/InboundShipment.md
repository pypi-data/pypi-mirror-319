# InboundShipment

Represents an AWD inbound shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_code** | [**CarrierCode**](CarrierCode.md) |  | [optional] 
**created_at** | **datetime** | Timestamp when the shipment was created. The date is returned in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
**destination_address** | [**Address**](Address.md) |  | 
**external_reference_id** | **str** | Client-provided reference ID that can correlate this shipment to client resources. For example, to map this shipment to an internal bookkeeping order record. | [optional] 
**order_id** | **str** | The AWD inbound order ID that this inbound shipment belongs to. | 
**origin_address** | [**Address**](Address.md) |  | 
**received_quantity** | [**List[InventoryQuantity]**](InventoryQuantity.md) | Quantity received (at the receiving end) as part of this shipment. | [optional] 
**ship_by** | **datetime** | Timestamp when the shipment will be shipped. | [optional] 
**shipment_container_quantities** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | Packages that are part of this shipment. | 
**shipment_id** | **str** | Unique shipment ID. | 
**shipment_sku_quantities** | [**List[SkuQuantity]**](SkuQuantity.md) | Quantity details at SKU level for the shipment. This attribute will only appear if the skuQuantities parameter in the request is set to SHOW. | [optional] 
**destination_region** | **str** | Assigned region where the order will be shipped. This can differ from what was passed as preference. AWD currently supports following region IDs: [us-west, us-east] | [optional] 
**shipment_status** | [**InboundShipmentStatus**](InboundShipmentStatus.md) |  | 
**tracking_id** | **str** | Carrier-unique tracking ID for this shipment. | [optional] 
**updated_at** | **datetime** | Timestamp when the shipment was updated. The date is returned in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
**warehouse_reference_id** | **str** | An AWD-provided reference ID that you can use to interact with the warehouse. For example, a carrier appointment booking. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_shipment import InboundShipment

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipment from a JSON string
inbound_shipment_instance = InboundShipment.from_json(json)
# print the JSON string representation of the object
print(InboundShipment.to_json())

# convert the object into a dict
inbound_shipment_dict = inbound_shipment_instance.to_dict()
# create an instance of InboundShipment from a dict
inbound_shipment_from_dict = InboundShipment.from_dict(inbound_shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


