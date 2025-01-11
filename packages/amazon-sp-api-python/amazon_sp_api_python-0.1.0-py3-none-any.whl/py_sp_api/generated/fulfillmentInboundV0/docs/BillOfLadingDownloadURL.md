# BillOfLadingDownloadURL

Download URL for the bill of lading.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**download_url** | **str** | URL to download the bill of lading for the package. Note: The URL will only be valid for 15 seconds | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.bill_of_lading_download_url import BillOfLadingDownloadURL

# TODO update the JSON string below
json = "{}"
# create an instance of BillOfLadingDownloadURL from a JSON string
bill_of_lading_download_url_instance = BillOfLadingDownloadURL.from_json(json)
# print the JSON string representation of the object
print(BillOfLadingDownloadURL.to_json())

# convert the object into a dict
bill_of_lading_download_url_dict = bill_of_lading_download_url_instance.to_dict()
# create an instance of BillOfLadingDownloadURL from a dict
bill_of_lading_download_url_from_dict = BillOfLadingDownloadURL.from_dict(bill_of_lading_download_url_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


