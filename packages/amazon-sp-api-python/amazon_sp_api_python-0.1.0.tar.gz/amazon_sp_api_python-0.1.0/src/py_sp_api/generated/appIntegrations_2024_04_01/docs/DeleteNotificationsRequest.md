# DeleteNotificationsRequest

The request for the `deleteNotifications` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template_id** | **str** | The unique identifier of the notification template you used to onboard your application. | 
**deletion_reason** | **str** | The unique identifier that maps each notification status to a reason code. | 

## Example

```python
from py_sp_api.generated.appIntegrations_2024_04_01.models.delete_notifications_request import DeleteNotificationsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteNotificationsRequest from a JSON string
delete_notifications_request_instance = DeleteNotificationsRequest.from_json(json)
# print the JSON string representation of the object
print(DeleteNotificationsRequest.to_json())

# convert the object into a dict
delete_notifications_request_dict = delete_notifications_request_instance.to_dict()
# create an instance of DeleteNotificationsRequest from a dict
delete_notifications_request_from_dict = DeleteNotificationsRequest.from_dict(delete_notifications_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


