# GetPackageTrackingDetailsResponse

The response schema for the `getPackageTrackingDetails` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**PackageTrackingDetails**](PackageTrackingDetails.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_package_tracking_details_response import GetPackageTrackingDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPackageTrackingDetailsResponse from a JSON string
get_package_tracking_details_response_instance = GetPackageTrackingDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(GetPackageTrackingDetailsResponse.to_json())

# convert the object into a dict
get_package_tracking_details_response_dict = get_package_tracking_details_response_instance.to_dict()
# create an instance of GetPackageTrackingDetailsResponse from a dict
get_package_tracking_details_response_from_dict = GetPackageTrackingDetailsResponse.from_dict(get_package_tracking_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


