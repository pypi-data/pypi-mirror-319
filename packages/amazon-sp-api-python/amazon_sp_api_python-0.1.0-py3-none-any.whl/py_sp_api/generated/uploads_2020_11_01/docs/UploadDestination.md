# UploadDestination

Information about an upload destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_destination_id** | **str** | The unique identifier for the upload destination. | [optional] 
**url** | **str** | The URL for the upload destination. | [optional] 
**headers** | **object** | The headers to include in the upload request. | [optional] 

## Example

```python
from py_sp_api.generated.uploads_2020_11_01.models.upload_destination import UploadDestination

# TODO update the JSON string below
json = "{}"
# create an instance of UploadDestination from a JSON string
upload_destination_instance = UploadDestination.from_json(json)
# print the JSON string representation of the object
print(UploadDestination.to_json())

# convert the object into a dict
upload_destination_dict = upload_destination_instance.to_dict()
# create an instance of UploadDestination from a dict
upload_destination_from_dict = UploadDestination.from_dict(upload_destination_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


