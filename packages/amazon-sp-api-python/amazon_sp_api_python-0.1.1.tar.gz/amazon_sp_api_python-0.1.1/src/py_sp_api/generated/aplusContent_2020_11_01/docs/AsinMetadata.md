# AsinMetadata

The A+ Content ASIN with additional metadata for content management. If you don't include the `includedDataSet` parameter in a call to the listContentDocumentAsinRelations operation, the related ASINs are returned without metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN). | 
**badge_set** | [**List[AsinBadge]**](AsinBadge.md) | The set of ASIN badges. | [optional] 
**parent** | **str** | The Amazon Standard Identification Number (ASIN). | [optional] 
**title** | **str** | The title for the ASIN in the Amazon catalog. | [optional] 
**image_url** | **str** | The default image for the ASIN in the Amazon catalog. | [optional] 
**content_reference_key_set** | **List[str]** | A set of content reference keys. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.asin_metadata import AsinMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of AsinMetadata from a JSON string
asin_metadata_instance = AsinMetadata.from_json(json)
# print the JSON string representation of the object
print(AsinMetadata.to_json())

# convert the object into a dict
asin_metadata_dict = asin_metadata_instance.to_dict()
# create an instance of AsinMetadata from a dict
asin_metadata_from_dict = AsinMetadata.from_dict(asin_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


