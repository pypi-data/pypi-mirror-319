# ContentMetadataRecord

The metadata for an A+ Content document, with additional information for content management.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_reference_key** | **str** | A unique reference key for the A+ Content document. A content reference key cannot form a permalink and may change in the future. A content reference key is not guaranteed to match any A+ content identifier. | 
**content_metadata** | [**ContentMetadata**](ContentMetadata.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.content_metadata_record import ContentMetadataRecord

# TODO update the JSON string below
json = "{}"
# create an instance of ContentMetadataRecord from a JSON string
content_metadata_record_instance = ContentMetadataRecord.from_json(json)
# print the JSON string representation of the object
print(ContentMetadataRecord.to_json())

# convert the object into a dict
content_metadata_record_dict = content_metadata_record_instance.to_dict()
# create an instance of ContentMetadataRecord from a dict
content_metadata_record_from_dict = ContentMetadataRecord.from_dict(content_metadata_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


