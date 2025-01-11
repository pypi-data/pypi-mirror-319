# DocumentDownload

Resource to download the requested document.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**download_type** | **str** | The type of download. Possible values: &#x60;URL&#x60;. | 
**expiration** | **datetime** | The URI&#39;s expiration time. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ss.sssZ&#x60;. | [optional] 
**uri** | **str** | Uniform resource identifier to identify where the document is located. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.document_download import DocumentDownload

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentDownload from a JSON string
document_download_instance = DocumentDownload.from_json(json)
# print the JSON string representation of the object
print(DocumentDownload.to_json())

# convert the object into a dict
document_download_dict = document_download_instance.to_dict()
# create an instance of DocumentDownload from a dict
document_download_from_dict = DocumentDownload.from_dict(document_download_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


