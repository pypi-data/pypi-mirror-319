# CreateScheduledPackagesRequest

The request body for the POST /easyShip/2022-03-23/packages/bulk API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A string of up to 255 characters. | 
**order_schedule_details_list** | [**List[OrderScheduleDetails]**](OrderScheduleDetails.md) | An array allowing users to specify orders to be scheduled. | 
**label_format** | [**LabelFormat**](LabelFormat.md) |  | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_packages_request import CreateScheduledPackagesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateScheduledPackagesRequest from a JSON string
create_scheduled_packages_request_instance = CreateScheduledPackagesRequest.from_json(json)
# print the JSON string representation of the object
print(CreateScheduledPackagesRequest.to_json())

# convert the object into a dict
create_scheduled_packages_request_dict = create_scheduled_packages_request_instance.to_dict()
# create an instance of CreateScheduledPackagesRequest from a dict
create_scheduled_packages_request_from_dict = CreateScheduledPackagesRequest.from_dict(create_scheduled_packages_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


