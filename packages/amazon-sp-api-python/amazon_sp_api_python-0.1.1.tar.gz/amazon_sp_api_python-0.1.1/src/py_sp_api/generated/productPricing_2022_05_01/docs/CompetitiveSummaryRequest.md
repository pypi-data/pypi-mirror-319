# CompetitiveSummaryRequest

An individual `competitiveSummary` request for an ASIN and `marketplaceId`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The ASIN of the item. | 
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which data is returned. | 
**included_data** | [**List[CompetitiveSummaryIncludedData]**](CompetitiveSummaryIncludedData.md) | The list of requested competitive pricing data for the product. | 
**lowest_priced_offers_inputs** | [**List[LowestPricedOffersInput]**](LowestPricedOffersInput.md) | The list of &#x60;lowestPricedOffersInput&#x60; parameters that are used to build &#x60;lowestPricedOffers&#x60; in the response. This attribute is only valid if &#x60;lowestPricedOffers&#x60; is requested in &#x60;includedData&#x60; | [optional] 
**method** | [**HttpMethod**](HttpMethod.md) |  | 
**uri** | **str** | The URI associated with the individual APIs that are called as part of the batch request. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.competitive_summary_request import CompetitiveSummaryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitiveSummaryRequest from a JSON string
competitive_summary_request_instance = CompetitiveSummaryRequest.from_json(json)
# print the JSON string representation of the object
print(CompetitiveSummaryRequest.to_json())

# convert the object into a dict
competitive_summary_request_dict = competitive_summary_request_instance.to_dict()
# create an instance of CompetitiveSummaryRequest from a dict
competitive_summary_request_from_dict = CompetitiveSummaryRequest.from_dict(competitive_summary_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


