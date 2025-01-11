# GetAccessPointsResponse

The response schema for the GetAccessPoints operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetAccessPointsResult**](GetAccessPointsResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_access_points_response import GetAccessPointsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccessPointsResponse from a JSON string
get_access_points_response_instance = GetAccessPointsResponse.from_json(json)
# print the JSON string representation of the object
print(GetAccessPointsResponse.to_json())

# convert the object into a dict
get_access_points_response_dict = get_access_points_response_instance.to_dict()
# create an instance of GetAccessPointsResponse from a dict
get_access_points_response_from_dict = GetAccessPointsResponse.from_dict(get_access_points_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


