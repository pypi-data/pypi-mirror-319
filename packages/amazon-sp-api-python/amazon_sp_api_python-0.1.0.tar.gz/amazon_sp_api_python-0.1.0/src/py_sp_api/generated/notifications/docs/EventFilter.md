# EventFilter

A `notificationType` specific filter. This object contains all of the currently available filters and properties that you can use to define a `notificationType` specific filter.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_settings** | [**AggregationSettings**](AggregationSettings.md) |  | [optional] 
**marketplace_ids** | **List[str]** | A list of marketplace identifiers to subscribe to (for example: ATVPDKIKX0DER). To receive notifications in every marketplace, do not provide this list. | [optional] 
**order_change_types** | [**List[OrderChangeTypeEnum]**](OrderChangeTypeEnum.md) | A list of order change types to subscribe to (for example: &#x60;BuyerRequestedChange&#x60;). To receive notifications of all change types, do not provide this list. | [optional] 
**event_filter_type** | **str** | An &#x60;eventFilterType&#x60; value that is supported by the specific &#x60;notificationType&#x60;. This is used by the subscription service to determine the type of event filter. Refer to [Notification Type Values](https://developer-docs.amazon.com/sp-api/docs/notification-type-values) to determine if an &#x60;eventFilterType&#x60; is supported. | 

## Example

```python
from py_sp_api.generated.notifications.models.event_filter import EventFilter

# TODO update the JSON string below
json = "{}"
# create an instance of EventFilter from a JSON string
event_filter_instance = EventFilter.from_json(json)
# print the JSON string representation of the object
print(EventFilter.to_json())

# convert the object into a dict
event_filter_dict = event_filter_instance.to_dict()
# create an instance of EventFilter from a dict
event_filter_from_dict = EventFilter.from_dict(event_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


