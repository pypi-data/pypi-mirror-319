# GetFeaturesResult

The payload for the `getFeatures` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**features** | [**List[Feature]**](Feature.md) | An array of features. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_features_result import GetFeaturesResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeaturesResult from a JSON string
get_features_result_instance = GetFeaturesResult.from_json(json)
# print the JSON string representation of the object
print(GetFeaturesResult.to_json())

# convert the object into a dict
get_features_result_dict = get_features_result_instance.to_dict()
# create an instance of GetFeaturesResult from a dict
get_features_result_from_dict = GetFeaturesResult.from_dict(get_features_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


