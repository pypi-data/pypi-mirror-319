# CreateScheduledPackageRequest

The request schema for the `createScheduledPackage` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**marketplace_id** | **str** | A string of up to 255 characters. | 
**package_details** | [**PackageDetails**](PackageDetails.md) |  | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_package_request import CreateScheduledPackageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateScheduledPackageRequest from a JSON string
create_scheduled_package_request_instance = CreateScheduledPackageRequest.from_json(json)
# print the JSON string representation of the object
print(CreateScheduledPackageRequest.to_json())

# convert the object into a dict
create_scheduled_package_request_dict = create_scheduled_package_request_instance.to_dict()
# create an instance of CreateScheduledPackageRequest from a dict
create_scheduled_package_request_from_dict = CreateScheduledPackageRequest.from_dict(create_scheduled_package_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


