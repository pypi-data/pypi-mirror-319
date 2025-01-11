# ScheduledDeliveryInfo

Delivery information for a scheduled delivery. This is only available in the JP marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_time_zone** | **str** | The time zone of the destination address for the fulfillment order preview. Must be an IANA time zone name. Example: Asia/Tokyo. | 
**delivery_windows** | [**List[DeliveryWindow]**](DeliveryWindow.md) | An array of delivery windows. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.scheduled_delivery_info import ScheduledDeliveryInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduledDeliveryInfo from a JSON string
scheduled_delivery_info_instance = ScheduledDeliveryInfo.from_json(json)
# print the JSON string representation of the object
print(ScheduledDeliveryInfo.to_json())

# convert the object into a dict
scheduled_delivery_info_dict = scheduled_delivery_info_instance.to_dict()
# create an instance of ScheduledDeliveryInfo from a dict
scheduled_delivery_info_from_dict = ScheduledDeliveryInfo.from_dict(scheduled_delivery_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


