# GenerateCollectionFormResponse

The Response  for the GenerateCollectionFormResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collections_form_document** | [**CollectionsFormDocument**](CollectionsFormDocument.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.generate_collection_form_response import GenerateCollectionFormResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateCollectionFormResponse from a JSON string
generate_collection_form_response_instance = GenerateCollectionFormResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateCollectionFormResponse.to_json())

# convert the object into a dict
generate_collection_form_response_dict = generate_collection_form_response_instance.to_dict()
# create an instance of GenerateCollectionFormResponse from a dict
generate_collection_form_response_from_dict = GenerateCollectionFormResponse.from_dict(generate_collection_form_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


