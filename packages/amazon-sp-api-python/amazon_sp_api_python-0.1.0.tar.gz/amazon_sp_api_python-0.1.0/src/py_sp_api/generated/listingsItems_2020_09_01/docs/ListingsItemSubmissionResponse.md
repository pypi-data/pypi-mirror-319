# ListingsItemSubmissionResponse

Response containing the results of a submission to the Selling Partner API for Listings Items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku** | **str** | A selling partner provided identifier for an Amazon listing. | 
**status** | **str** | The status of the listings item submission. | 
**submission_id** | **str** | The unique identifier of the listings item submission. | 
**issues** | [**List[Issue]**](Issue.md) | Listings item issues related to the listings item submission. | [optional] 

## Example

```python
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_submission_response import ListingsItemSubmissionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListingsItemSubmissionResponse from a JSON string
listings_item_submission_response_instance = ListingsItemSubmissionResponse.from_json(json)
# print the JSON string representation of the object
print(ListingsItemSubmissionResponse.to_json())

# convert the object into a dict
listings_item_submission_response_dict = listings_item_submission_response_instance.to_dict()
# create an instance of ListingsItemSubmissionResponse from a dict
listings_item_submission_response_from_dict = ListingsItemSubmissionResponse.from_dict(listings_item_submission_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


