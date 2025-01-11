# CreateNotificationResponse

The response for the `createNotification` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notification_id** | **str** | The unique identifier assigned to each notification. | [optional] 

## Example

```python
from py_sp_api.generated.appIntegrations_2024_04_01.models.create_notification_response import CreateNotificationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateNotificationResponse from a JSON string
create_notification_response_instance = CreateNotificationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateNotificationResponse.to_json())

# convert the object into a dict
create_notification_response_dict = create_notification_response_instance.to_dict()
# create an instance of CreateNotificationResponse from a dict
create_notification_response_from_dict = CreateNotificationResponse.from_dict(create_notification_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


