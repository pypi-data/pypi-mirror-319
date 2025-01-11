# UpdateScheduledPackagesRequest

The request schema for the `updateScheduledPackages` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A string of up to 255 characters. | 
**update_package_details_list** | [**List[UpdatePackageDetails]**](UpdatePackageDetails.md) | A list of package update details. | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.update_scheduled_packages_request import UpdateScheduledPackagesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScheduledPackagesRequest from a JSON string
update_scheduled_packages_request_instance = UpdateScheduledPackagesRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateScheduledPackagesRequest.to_json())

# convert the object into a dict
update_scheduled_packages_request_dict = update_scheduled_packages_request_instance.to_dict()
# create an instance of UpdateScheduledPackagesRequest from a dict
update_scheduled_packages_request_from_dict = UpdateScheduledPackagesRequest.from_dict(update_scheduled_packages_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


