# BatchResponse

The common properties for responses to individual requests within a batch.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | **Dict[str, str]** | A mapping of additional HTTP headers to send or receive for an individual request within a batch. | 
**status** | [**HttpStatusLine**](HttpStatusLine.md) |  | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.batch_response import BatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BatchResponse from a JSON string
batch_response_instance = BatchResponse.from_json(json)
# print the JSON string representation of the object
print(BatchResponse.to_json())

# convert the object into a dict
batch_response_dict = batch_response_instance.to_dict()
# create an instance of BatchResponse from a dict
batch_response_from_dict = BatchResponse.from_dict(batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


