# GetAccessPointsResult

The payload for the GetAccessPoints API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_points_map** | **Dict[str, List[AccessPoint]]** | Map of type of access point to list of access points | 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_access_points_result import GetAccessPointsResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetAccessPointsResult from a JSON string
get_access_points_result_instance = GetAccessPointsResult.from_json(json)
# print the JSON string representation of the object
print(GetAccessPointsResult.to_json())

# convert the object into a dict
get_access_points_result_dict = get_access_points_result_instance.to_dict()
# create an instance of GetAccessPointsResult from a dict
get_access_points_result_from_dict = GetAccessPointsResult.from_dict(get_access_points_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


