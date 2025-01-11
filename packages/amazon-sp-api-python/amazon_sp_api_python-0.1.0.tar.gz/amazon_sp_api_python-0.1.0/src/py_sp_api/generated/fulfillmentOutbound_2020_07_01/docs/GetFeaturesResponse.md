# GetFeaturesResponse

The response schema for the `getFeatures` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetFeaturesResult**](GetFeaturesResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_features_response import GetFeaturesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeaturesResponse from a JSON string
get_features_response_instance = GetFeaturesResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeaturesResponse.to_json())

# convert the object into a dict
get_features_response_dict = get_features_response_instance.to_dict()
# create an instance of GetFeaturesResponse from a dict
get_features_response_from_dict = GetFeaturesResponse.from_dict(get_features_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


