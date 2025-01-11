# SellerFeedbackType

Information about the seller's feedback, including the percentage of positive feedback, and the total number of ratings received.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_positive_feedback_rating** | **float** | The percentage of positive feedback for the seller in the past 365 days. | [optional] 
**feedback_count** | **int** | The number of ratings received about the seller. | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.seller_feedback_type import SellerFeedbackType

# TODO update the JSON string below
json = "{}"
# create an instance of SellerFeedbackType from a JSON string
seller_feedback_type_instance = SellerFeedbackType.from_json(json)
# print the JSON string representation of the object
print(SellerFeedbackType.to_json())

# convert the object into a dict
seller_feedback_type_dict = seller_feedback_type_instance.to_dict()
# create an instance of SellerFeedbackType from a dict
seller_feedback_type_from_dict = SellerFeedbackType.from_dict(seller_feedback_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


