# CompetitiveSummaryResponseBody

The `competitiveSummaryResponse` body for a requested ASIN and `marketplaceId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The ASIN of the item. | 
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which data is returned. | 
**featured_buying_options** | [**List[FeaturedBuyingOption]**](FeaturedBuyingOption.md) | A list of featured buying options for the specified ASIN &#x60;marketplaceId&#x60; combination. | [optional] 
**lowest_priced_offers** | [**List[LowestPricedOffer]**](LowestPricedOffer.md) | A list of lowest priced offers for the specified ASIN &#x60;marketplaceId&#x60; combination. | [optional] 
**reference_prices** | [**List[ReferencePrice]**](ReferencePrice.md) | A list of reference prices for the specified ASIN &#x60;marketplaceId&#x60; combination. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses that are returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.competitive_summary_response_body import CompetitiveSummaryResponseBody

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitiveSummaryResponseBody from a JSON string
competitive_summary_response_body_instance = CompetitiveSummaryResponseBody.from_json(json)
# print the JSON string representation of the object
print(CompetitiveSummaryResponseBody.to_json())

# convert the object into a dict
competitive_summary_response_body_dict = competitive_summary_response_body_instance.to_dict()
# create an instance of CompetitiveSummaryResponseBody from a dict
competitive_summary_response_body_from_dict = CompetitiveSummaryResponseBody.from_dict(competitive_summary_response_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


