# ScheduledPackageId

Identifies the scheduled package to be updated.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**package_id** | **str** | An Amazon-defined identifier for the scheduled package. | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.scheduled_package_id import ScheduledPackageId

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduledPackageId from a JSON string
scheduled_package_id_instance = ScheduledPackageId.from_json(json)
# print the JSON string representation of the object
print(ScheduledPackageId.to_json())

# convert the object into a dict
scheduled_package_id_dict = scheduled_package_id_instance.to_dict()
# create an instance of ScheduledPackageId from a dict
scheduled_package_id_from_dict = ScheduledPackageId.from_dict(scheduled_package_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


