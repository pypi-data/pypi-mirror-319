# GetFeatureSkuResult

The payload for the `getFeatureSKU` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The requested marketplace. | 
**feature_name** | **str** | The name of the feature. | 
**is_eligible** | **bool** | When true, the seller SKU is eligible for the requested feature. | 
**ineligible_reasons** | **List[str]** | A list of one or more reasons that the seller SKU is ineligibile for the feature.  Possible values: * &#x60;MERCHANT_NOT_ENROLLED&#x60; - The merchant isn&#39;t enrolled for the feature. * &#x60;SKU_NOT_ELIGIBLE&#x60; - The SKU doesn&#39;t reside in a warehouse that supports the feature. * &#x60;INVALID_SKU&#x60; - There is an issue with the SKU provided. | [optional] 
**sku_info** | [**FeatureSku**](FeatureSku.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_feature_sku_result import GetFeatureSkuResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureSkuResult from a JSON string
get_feature_sku_result_instance = GetFeatureSkuResult.from_json(json)
# print the JSON string representation of the object
print(GetFeatureSkuResult.to_json())

# convert the object into a dict
get_feature_sku_result_dict = get_feature_sku_result_instance.to_dict()
# create an instance of GetFeatureSkuResult from a dict
get_feature_sku_result_from_dict = GetFeatureSkuResult.from_dict(get_feature_sku_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


