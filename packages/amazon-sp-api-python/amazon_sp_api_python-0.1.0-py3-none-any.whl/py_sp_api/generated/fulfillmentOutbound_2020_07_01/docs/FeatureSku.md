# FeatureSku

Information about an SKU, including the count available, identifiers, and a list of overlapping SKUs that share the same inventory pool.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | Used to identify an item in the given marketplace. &#x60;SellerSKU&#x60; is qualified by the seller&#39;s SellerId, which is included with every operation that you submit. | [optional] 
**fn_sku** | **str** | The unique SKU used by Amazon&#39;s fulfillment network. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**sku_count** | **float** | The number of SKUs available for this service. | [optional] 
**overlapping_skus** | **List[str]** | Other seller SKUs that are shared across the same inventory. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.feature_sku import FeatureSku

# TODO update the JSON string below
json = "{}"
# create an instance of FeatureSku from a JSON string
feature_sku_instance = FeatureSku.from_json(json)
# print the JSON string representation of the object
print(FeatureSku.to_json())

# convert the object into a dict
feature_sku_dict = feature_sku_instance.to_dict()
# create an instance of FeatureSku from a dict
feature_sku_from_dict = FeatureSku.from_dict(feature_sku_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


