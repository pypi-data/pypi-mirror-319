# CreateProductReviewAndSellerFeedbackSolicitationResponse

The response schema for the createProductReviewAndSellerFeedbackSolicitation operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.solicitations.models.create_product_review_and_seller_feedback_solicitation_response import CreateProductReviewAndSellerFeedbackSolicitationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateProductReviewAndSellerFeedbackSolicitationResponse from a JSON string
create_product_review_and_seller_feedback_solicitation_response_instance = CreateProductReviewAndSellerFeedbackSolicitationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateProductReviewAndSellerFeedbackSolicitationResponse.to_json())

# convert the object into a dict
create_product_review_and_seller_feedback_solicitation_response_dict = create_product_review_and_seller_feedback_solicitation_response_instance.to_dict()
# create an instance of CreateProductReviewAndSellerFeedbackSolicitationResponse from a dict
create_product_review_and_seller_feedback_solicitation_response_from_dict = CreateProductReviewAndSellerFeedbackSolicitationResponse.from_dict(create_product_review_and_seller_feedback_solicitation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


