# GetFeatureSkuResponse

The response schema for the `getFeatureSKU` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetFeatureSkuResult**](GetFeatureSkuResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_feature_sku_response import GetFeatureSkuResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureSkuResponse from a JSON string
get_feature_sku_response_instance = GetFeatureSkuResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeatureSkuResponse.to_json())

# convert the object into a dict
get_feature_sku_response_dict = get_feature_sku_response_instance.to_dict()
# create an instance of GetFeatureSkuResponse from a dict
get_feature_sku_response_from_dict = GetFeatureSkuResponse.from_dict(get_feature_sku_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


