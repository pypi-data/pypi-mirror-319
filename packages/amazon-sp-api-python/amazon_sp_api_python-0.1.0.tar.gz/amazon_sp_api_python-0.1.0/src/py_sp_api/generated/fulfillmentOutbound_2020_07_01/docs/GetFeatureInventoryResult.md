# GetFeatureInventoryResult

The payload for the `getEligibileInventory` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The requested marketplace. | 
**feature_name** | **str** | The name of the feature. | 
**next_token** | **str** | When present and not empty, pass this string token in the next request to return the next response page. | [optional] 
**feature_skus** | [**List[FeatureSku]**](FeatureSku.md) | An array of SKUs eligible for this feature and the quantity available. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_feature_inventory_result import GetFeatureInventoryResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureInventoryResult from a JSON string
get_feature_inventory_result_instance = GetFeatureInventoryResult.from_json(json)
# print the JSON string representation of the object
print(GetFeatureInventoryResult.to_json())

# convert the object into a dict
get_feature_inventory_result_dict = get_feature_inventory_result_instance.to_dict()
# create an instance of GetFeatureInventoryResult from a dict
get_feature_inventory_result_from_dict = GetFeatureInventoryResult.from_dict(get_feature_inventory_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


