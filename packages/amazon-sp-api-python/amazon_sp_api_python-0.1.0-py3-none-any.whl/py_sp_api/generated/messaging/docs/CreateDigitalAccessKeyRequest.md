# CreateDigitalAccessKeyRequest

The request schema for the `createDigitalAccessKey` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text that is sent to the buyer. Only links that are related to the digital access key are allowed. Do not include HTML or email addresses. The text must be written in the buyer&#39;s preferred language, which you can retrieve from the &#x60;GetAttributes&#x60; operation. | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) | Attachments that you want to include in the message to the buyer. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_digital_access_key_request import CreateDigitalAccessKeyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDigitalAccessKeyRequest from a JSON string
create_digital_access_key_request_instance = CreateDigitalAccessKeyRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDigitalAccessKeyRequest.to_json())

# convert the object into a dict
create_digital_access_key_request_dict = create_digital_access_key_request_instance.to_dict()
# create an instance of CreateDigitalAccessKeyRequest from a dict
create_digital_access_key_request_from_dict = CreateDigitalAccessKeyRequest.from_dict(create_digital_access_key_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


