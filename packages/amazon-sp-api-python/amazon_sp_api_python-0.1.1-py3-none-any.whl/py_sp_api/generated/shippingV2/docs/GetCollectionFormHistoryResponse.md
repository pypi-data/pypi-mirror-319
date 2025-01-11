# GetCollectionFormHistoryResponse

The Response  for the GetCollectionFormHistoryResponse operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection_forms_history_record_list** | [**List[CollectionFormsHistoryRecord]**](CollectionFormsHistoryRecord.md) | A list of CollectionFormsHistoryRecord | [optional] 
**last_refreshed_date** | **str** | Last Refereshed Date of collection | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_collection_form_history_response import GetCollectionFormHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCollectionFormHistoryResponse from a JSON string
get_collection_form_history_response_instance = GetCollectionFormHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(GetCollectionFormHistoryResponse.to_json())

# convert the object into a dict
get_collection_form_history_response_dict = get_collection_form_history_response_instance.to_dict()
# create an instance of GetCollectionFormHistoryResponse from a dict
get_collection_form_history_response_from_dict = GetCollectionFormHistoryResponse.from_dict(get_collection_form_history_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


