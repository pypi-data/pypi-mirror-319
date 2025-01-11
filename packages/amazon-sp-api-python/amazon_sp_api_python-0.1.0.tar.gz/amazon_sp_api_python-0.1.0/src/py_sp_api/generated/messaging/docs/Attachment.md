# Attachment

Represents a file that was uploaded to a destination that was created by the Uploads API [`createUploadDestinationForResource`](https://developer-docs.amazon.com/sp-api/docs/uploads-api-reference#post-uploads2020-11-01uploaddestinationsresource) operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_destination_id** | **str** | The identifier for the upload destination. To retrieve this value, call the Uploads API [&#x60;createUploadDestinationForResource&#x60;](https://developer-docs.amazon.com/sp-api/docs/uploads-api-reference#post-uploads2020-11-01uploaddestinationsresource) operation. | 
**file_name** | **str** | The name of the file, including the extension. This is the file name that will appear in the message. This does not need to match the file name of the file that you uploaded. | 

## Example

```python
from py_sp_api.generated.messaging.models.attachment import Attachment

# TODO update the JSON string below
json = "{}"
# create an instance of Attachment from a JSON string
attachment_instance = Attachment.from_json(json)
# print the JSON string representation of the object
print(Attachment.to_json())

# convert the object into a dict
attachment_dict = attachment_instance.to_dict()
# create an instance of Attachment from a dict
attachment_from_dict = Attachment.from_dict(attachment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


