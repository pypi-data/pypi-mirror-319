# ContentMetadata

The metadata of an A+ Content document.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The A+ Content document name. | 
**marketplace_id** | **str** | The identifier for the marketplace where the A+ Content is published. | 
**status** | [**ContentStatus**](ContentStatus.md) |  | 
**badge_set** | [**List[ContentBadge]**](ContentBadge.md) | The set of content badges. | 
**update_time** | **datetime** | The approximate age of the A+ Content document and metadata. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.content_metadata import ContentMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ContentMetadata from a JSON string
content_metadata_instance = ContentMetadata.from_json(json)
# print the JSON string representation of the object
print(ContentMetadata.to_json())

# convert the object into a dict
content_metadata_dict = content_metadata_instance.to_dict()
# create an instance of ContentMetadata from a dict
content_metadata_from_dict = ContentMetadata.from_dict(content_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


