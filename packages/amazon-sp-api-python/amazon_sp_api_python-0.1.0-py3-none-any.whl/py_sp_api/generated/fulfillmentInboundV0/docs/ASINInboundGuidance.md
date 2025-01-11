# ASINInboundGuidance

Reasons why a given ASIN is not recommended for shipment to Amazon's fulfillment network.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | 
**inbound_guidance** | [**InboundGuidance**](InboundGuidance.md) |  | 
**guidance_reason_list** | [**List[GuidanceReason]**](GuidanceReason.md) | A list of inbound guidance reason information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.asin_inbound_guidance import ASINInboundGuidance

# TODO update the JSON string below
json = "{}"
# create an instance of ASINInboundGuidance from a JSON string
asin_inbound_guidance_instance = ASINInboundGuidance.from_json(json)
# print the JSON string representation of the object
print(ASINInboundGuidance.to_json())

# convert the object into a dict
asin_inbound_guidance_dict = asin_inbound_guidance_instance.to_dict()
# create an instance of ASINInboundGuidance from a dict
asin_inbound_guidance_from_dict = ASINInboundGuidance.from_dict(asin_inbound_guidance_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


