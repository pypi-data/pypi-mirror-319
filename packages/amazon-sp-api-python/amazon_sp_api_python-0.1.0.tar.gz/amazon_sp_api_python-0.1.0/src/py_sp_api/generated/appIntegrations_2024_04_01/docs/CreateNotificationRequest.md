# CreateNotificationRequest

The request for the `createNotification` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template_id** | **str** | The unique identifier of the notification template you used to onboard your application. | 
**notification_parameters** | **Dict[str, object]** | The dynamic parameters required by the notification templated specified by &#x60;templateId&#x60;. | 
**marketplace_id** | **str** | An encrypted marketplace identifier for the posted notification. | [optional] 

## Example

```python
from py_sp_api.generated.appIntegrations_2024_04_01.models.create_notification_request import CreateNotificationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateNotificationRequest from a JSON string
create_notification_request_instance = CreateNotificationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateNotificationRequest.to_json())

# convert the object into a dict
create_notification_request_dict = create_notification_request_instance.to_dict()
# create an instance of CreateNotificationRequest from a dict
create_notification_request_from_dict = CreateNotificationRequest.from_dict(create_notification_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


