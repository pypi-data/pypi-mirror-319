# GetInboundGuidanceResult

Result for the get inbound guidance operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku_inbound_guidance_list** | [**List[SKUInboundGuidance]**](SKUInboundGuidance.md) | A list of SKU inbound guidance information. | [optional] 
**invalid_sku_list** | [**List[InvalidSKU]**](InvalidSKU.md) | A list of invalid SKU values and the reason they are invalid. | [optional] 
**asin_inbound_guidance_list** | [**List[ASINInboundGuidance]**](ASINInboundGuidance.md) | A list of ASINs and their associated inbound guidance. | [optional] 
**invalid_asin_list** | [**List[InvalidASIN]**](InvalidASIN.md) | A list of invalid ASIN values and the reasons they are invalid. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_inbound_guidance_result import GetInboundGuidanceResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetInboundGuidanceResult from a JSON string
get_inbound_guidance_result_instance = GetInboundGuidanceResult.from_json(json)
# print the JSON string representation of the object
print(GetInboundGuidanceResult.to_json())

# convert the object into a dict
get_inbound_guidance_result_dict = get_inbound_guidance_result_instance.to_dict()
# create an instance of GetInboundGuidanceResult from a dict
get_inbound_guidance_result_from_dict = GetInboundGuidanceResult.from_dict(get_inbound_guidance_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


