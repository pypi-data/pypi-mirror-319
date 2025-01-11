# SKUInboundGuidance

Reasons why a given seller SKU is not recommended for shipment to Amazon's fulfillment network.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | 
**inbound_guidance** | [**InboundGuidance**](InboundGuidance.md) |  | 
**guidance_reason_list** | [**List[GuidanceReason]**](GuidanceReason.md) | A list of inbound guidance reason information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.sku_inbound_guidance import SKUInboundGuidance

# TODO update the JSON string below
json = "{}"
# create an instance of SKUInboundGuidance from a JSON string
sku_inbound_guidance_instance = SKUInboundGuidance.from_json(json)
# print the JSON string representation of the object
print(SKUInboundGuidance.to_json())

# convert the object into a dict
sku_inbound_guidance_dict = sku_inbound_guidance_instance.to_dict()
# create an instance of SKUInboundGuidance from a dict
sku_inbound_guidance_from_dict = SKUInboundGuidance.from_dict(sku_inbound_guidance_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


