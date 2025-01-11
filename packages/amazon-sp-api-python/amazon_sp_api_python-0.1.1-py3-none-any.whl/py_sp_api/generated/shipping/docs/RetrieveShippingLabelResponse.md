# RetrieveShippingLabelResponse

The response schema for the retrieveShippingLabel operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**RetrieveShippingLabelResult**](RetrieveShippingLabelResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.retrieve_shipping_label_response import RetrieveShippingLabelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveShippingLabelResponse from a JSON string
retrieve_shipping_label_response_instance = RetrieveShippingLabelResponse.from_json(json)
# print the JSON string representation of the object
print(RetrieveShippingLabelResponse.to_json())

# convert the object into a dict
retrieve_shipping_label_response_dict = retrieve_shipping_label_response_instance.to_dict()
# create an instance of RetrieveShippingLabelResponse from a dict
retrieve_shipping_label_response_from_dict = RetrieveShippingLabelResponse.from_dict(retrieve_shipping_label_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


