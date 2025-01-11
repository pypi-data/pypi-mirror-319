# CollectionFormsHistoryRecord

Active Account Details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The carrier name for the offering. | [optional] 
**creation_date** | **str** | Creation Time for this account. | [optional] 
**generation_status** | [**GenerationStatus**](GenerationStatus.md) |  | [optional] 
**collection_form_id** | **str** | Collection Form Id for Reprint . | [optional] 
**ship_from_address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.collection_forms_history_record import CollectionFormsHistoryRecord

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionFormsHistoryRecord from a JSON string
collection_forms_history_record_instance = CollectionFormsHistoryRecord.from_json(json)
# print the JSON string representation of the object
print(CollectionFormsHistoryRecord.to_json())

# convert the object into a dict
collection_forms_history_record_dict = collection_forms_history_record_instance.to_dict()
# create an instance of CollectionFormsHistoryRecord from a dict
collection_forms_history_record_from_dict = CollectionFormsHistoryRecord.from_dict(collection_forms_history_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


