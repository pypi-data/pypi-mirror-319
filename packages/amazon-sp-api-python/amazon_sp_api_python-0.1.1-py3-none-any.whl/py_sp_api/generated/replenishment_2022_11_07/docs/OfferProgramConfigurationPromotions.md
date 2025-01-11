# OfferProgramConfigurationPromotions

An object which represents all promotions applied to an offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_partner_funded_base_discount** | [**OfferProgramConfigurationPromotionsDiscountFunding**](OfferProgramConfigurationPromotionsDiscountFunding.md) |  | [optional] 
**selling_partner_funded_tiered_discount** | [**OfferProgramConfigurationPromotionsDiscountFunding**](OfferProgramConfigurationPromotionsDiscountFunding.md) |  | [optional] 
**amazon_funded_base_discount** | [**OfferProgramConfigurationPromotionsDiscountFunding**](OfferProgramConfigurationPromotionsDiscountFunding.md) |  | [optional] 
**amazon_funded_tiered_discount** | [**OfferProgramConfigurationPromotionsDiscountFunding**](OfferProgramConfigurationPromotionsDiscountFunding.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.offer_program_configuration_promotions import OfferProgramConfigurationPromotions

# TODO update the JSON string below
json = "{}"
# create an instance of OfferProgramConfigurationPromotions from a JSON string
offer_program_configuration_promotions_instance = OfferProgramConfigurationPromotions.from_json(json)
# print the JSON string representation of the object
print(OfferProgramConfigurationPromotions.to_json())

# convert the object into a dict
offer_program_configuration_promotions_dict = offer_program_configuration_promotions_instance.to_dict()
# create an instance of OfferProgramConfigurationPromotions from a dict
offer_program_configuration_promotions_from_dict = OfferProgramConfigurationPromotions.from_dict(offer_program_configuration_promotions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


