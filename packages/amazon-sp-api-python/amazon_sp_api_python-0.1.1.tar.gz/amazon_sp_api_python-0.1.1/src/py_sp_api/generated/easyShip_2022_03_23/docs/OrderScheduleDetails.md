# OrderScheduleDetails

This object allows users to specify an order to be scheduled. Only the amazonOrderId is required. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**package_details** | [**PackageDetails**](PackageDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.order_schedule_details import OrderScheduleDetails

# TODO update the JSON string below
json = "{}"
# create an instance of OrderScheduleDetails from a JSON string
order_schedule_details_instance = OrderScheduleDetails.from_json(json)
# print the JSON string representation of the object
print(OrderScheduleDetails.to_json())

# convert the object into a dict
order_schedule_details_dict = order_schedule_details_instance.to_dict()
# create an instance of OrderScheduleDetails from a dict
order_schedule_details_from_dict = OrderScheduleDetails.from_dict(order_schedule_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


