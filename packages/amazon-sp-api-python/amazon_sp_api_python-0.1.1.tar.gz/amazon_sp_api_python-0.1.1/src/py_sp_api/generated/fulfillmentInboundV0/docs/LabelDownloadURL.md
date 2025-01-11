# LabelDownloadURL

Download URL for a label

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**download_url** | **str** | URL to download the label for the package. Note: The URL will only be valid for 15 seconds | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.label_download_url import LabelDownloadURL

# TODO update the JSON string below
json = "{}"
# create an instance of LabelDownloadURL from a JSON string
label_download_url_instance = LabelDownloadURL.from_json(json)
# print the JSON string representation of the object
print(LabelDownloadURL.to_json())

# convert the object into a dict
label_download_url_dict = label_download_url_instance.to_dict()
# create an instance of LabelDownloadURL from a dict
label_download_url_from_dict = LabelDownloadURL.from_dict(label_download_url_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


