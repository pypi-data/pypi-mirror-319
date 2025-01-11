# CreateWarrantyRequest

The request schema for the createWarranty operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attachments** | [**List[Attachment]**](Attachment.md) | Attachments to include in the message to the buyer. If any text is included in the attachment, the text must be written in the buyer&#39;s language of preference, which can be retrieved from the GetAttributes operation. | [optional] 
**coverage_start_date** | **datetime** | The start date of the warranty coverage to include in the message to the buyer. | [optional] 
**coverage_end_date** | **datetime** | The end date of the warranty coverage to include in the message to the buyer. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_warranty_request import CreateWarrantyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWarrantyRequest from a JSON string
create_warranty_request_instance = CreateWarrantyRequest.from_json(json)
# print the JSON string representation of the object
print(CreateWarrantyRequest.to_json())

# convert the object into a dict
create_warranty_request_dict = create_warranty_request_instance.to_dict()
# create an instance of CreateWarrantyRequest from a dict
create_warranty_request_from_dict = CreateWarrantyRequest.from_dict(create_warranty_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


