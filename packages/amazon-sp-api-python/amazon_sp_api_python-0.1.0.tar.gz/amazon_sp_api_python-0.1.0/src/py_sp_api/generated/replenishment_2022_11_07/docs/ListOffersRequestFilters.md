# ListOffersRequestFilters

Use these parameters to filter results. Any result must match all of the provided parameters. For any parameter that is an array, the result must match at least one element in the provided array.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The marketplace identifier. The supported marketplaces for both sellers and vendors are US, CA, ES, UK, FR, IT, IN, DE and JP. The supported marketplaces for vendors only are BR, AU, MX, AE and NL. Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) to find the identifier for the marketplace. | 
**skus** | **List[str]** | A list of SKUs to filter. This filter is only supported for sellers and not for vendors. | [optional] 
**asins** | **List[str]** | A list of Amazon Standard Identification Numbers (ASINs). | [optional] 
**eligibilities** | [**List[EligibilityStatus]**](EligibilityStatus.md) | A list of eligibilities associated with an offer. | [optional] 
**preferences** | [**Preference**](Preference.md) |  | [optional] 
**promotions** | [**Promotion**](Promotion.md) |  | [optional] 
**program_types** | [**List[ProgramType]**](ProgramType.md) | A list of replenishment program types. | 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offers_request_filters import ListOffersRequestFilters

# TODO update the JSON string below
json = "{}"
# create an instance of ListOffersRequestFilters from a JSON string
list_offers_request_filters_instance = ListOffersRequestFilters.from_json(json)
# print the JSON string representation of the object
print(ListOffersRequestFilters.to_json())

# convert the object into a dict
list_offers_request_filters_dict = list_offers_request_filters_instance.to_dict()
# create an instance of ListOffersRequestFilters from a dict
list_offers_request_filters_from_dict = ListOffersRequestFilters.from_dict(list_offers_request_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


