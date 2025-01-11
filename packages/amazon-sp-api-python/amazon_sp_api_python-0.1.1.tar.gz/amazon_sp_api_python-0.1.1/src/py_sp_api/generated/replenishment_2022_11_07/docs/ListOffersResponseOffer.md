# ListOffersResponseOffer

An object which contains details about an offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku** | **str** | The SKU. This property is only supported for sellers and not for vendors. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN). | [optional] 
**marketplace_id** | **str** | The marketplace identifier. The supported marketplaces for both sellers and vendors are US, CA, ES, UK, FR, IT, IN, DE and JP. The supported marketplaces for vendors only are BR, AU, MX, AE and NL. Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) to find the identifier for the marketplace. | [optional] 
**eligibility** | [**EligibilityStatus**](EligibilityStatus.md) |  | [optional] 
**offer_program_configuration** | [**OfferProgramConfiguration**](OfferProgramConfiguration.md) |  | [optional] 
**program_type** | [**ProgramType**](ProgramType.md) |  | [optional] 
**vendor_codes** | **List[str]** | A list of vendor codes associated with the offer. | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offers_response_offer import ListOffersResponseOffer

# TODO update the JSON string below
json = "{}"
# create an instance of ListOffersResponseOffer from a JSON string
list_offers_response_offer_instance = ListOffersResponseOffer.from_json(json)
# print the JSON string representation of the object
print(ListOffersResponseOffer.to_json())

# convert the object into a dict
list_offers_response_offer_dict = list_offers_response_offer_instance.to_dict()
# create an instance of ListOffersResponseOffer from a dict
list_offers_response_offer_from_dict = ListOffersResponseOffer.from_dict(list_offers_response_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


