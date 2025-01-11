# UpdatePackageDetails

Request to update the time slot of a package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scheduled_package_id** | [**ScheduledPackageId**](ScheduledPackageId.md) |  | 
**package_time_slot** | [**TimeSlot**](TimeSlot.md) |  | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.update_package_details import UpdatePackageDetails

# TODO update the JSON string below
json = "{}"
# create an instance of UpdatePackageDetails from a JSON string
update_package_details_instance = UpdatePackageDetails.from_json(json)
# print the JSON string representation of the object
print(UpdatePackageDetails.to_json())

# convert the object into a dict
update_package_details_dict = update_package_details_instance.to_dict()
# create an instance of UpdatePackageDetails from a dict
update_package_details_from_dict = UpdatePackageDetails.from_dict(update_package_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


