# ProcessingDirective

Additional information passed to the subscription to control the processing of notifications. For example, you can use an `eventFilter` to customize your subscription to send notifications for only the specified `marketplaceId`s, or select the aggregation time period at which to send notifications (for example: limit to one notification every five minutes for high frequency notifications). The specific features available vary depending on the `notificationType`.  This feature is currently only supported by the `ANY_OFFER_CHANGED` and `ORDER_CHANGE` `notificationType`s.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_filter** | [**EventFilter**](EventFilter.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.processing_directive import ProcessingDirective

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingDirective from a JSON string
processing_directive_instance = ProcessingDirective.from_json(json)
# print the JSON string representation of the object
print(ProcessingDirective.to_json())

# convert the object into a dict
processing_directive_dict = processing_directive_instance.to_dict()
# create an instance of ProcessingDirective from a dict
processing_directive_from_dict = ProcessingDirective.from_dict(processing_directive_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


