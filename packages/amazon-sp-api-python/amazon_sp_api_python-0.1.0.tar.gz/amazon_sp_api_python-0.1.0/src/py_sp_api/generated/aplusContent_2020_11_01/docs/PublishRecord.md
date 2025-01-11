# PublishRecord

The full context for an A+ Content publishing event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The identifier for the marketplace where the A+ Content is published. | 
**locale** | **str** | The IETF language tag. This only supports the primary language subtag with one secondary language subtag. The secondary language subtag is almost always a regional designation. This does not support additional subtags beyond the primary and secondary subtags. **Pattern:** ^[a-z]{2,}-[A-Z0-9]{2,}$ | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN). | 
**content_type** | [**ContentType**](ContentType.md) |  | 
**content_sub_type** | **str** | The A+ Content document subtype. This represents a special-purpose type of an A+ Content document. Not every A+ Content document type will have a subtype, and subtypes may change at any time. | [optional] 
**content_reference_key** | **str** | A unique reference key for the A+ Content document. A content reference key cannot form a permalink and may change in the future. A content reference key is not guaranteed to match any A+ content identifier. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.publish_record import PublishRecord

# TODO update the JSON string below
json = "{}"
# create an instance of PublishRecord from a JSON string
publish_record_instance = PublishRecord.from_json(json)
# print the JSON string representation of the object
print(PublishRecord.to_json())

# convert the object into a dict
publish_record_dict = publish_record_instance.to_dict()
# create an instance of PublishRecord from a dict
publish_record_from_dict = PublishRecord.from_dict(publish_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


