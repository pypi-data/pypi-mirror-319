# SqsResource

The information required to create an Amazon Simple Queue Service (Amazon SQS) queue destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arn** | **str** | The Amazon Resource Name (ARN) associated with the SQS queue. | 

## Example

```python
from py_sp_api.generated.notifications.models.sqs_resource import SqsResource

# TODO update the JSON string below
json = "{}"
# create an instance of SqsResource from a JSON string
sqs_resource_instance = SqsResource.from_json(json)
# print the JSON string representation of the object
print(SqsResource.to_json())

# convert the object into a dict
sqs_resource_dict = sqs_resource_instance.to_dict()
# create an instance of SqsResource from a dict
sqs_resource_from_dict = SqsResource.from_dict(sqs_resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


