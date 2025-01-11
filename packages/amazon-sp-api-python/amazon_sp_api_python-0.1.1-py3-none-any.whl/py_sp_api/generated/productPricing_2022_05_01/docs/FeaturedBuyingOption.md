# FeaturedBuyingOption

Describes a featured buying option, which includes a list of segmented featured offers for a particular item condition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buying_option_type** | **str** | The buying option type for the featured offer. &#x60;buyingOptionType&#x60; represents the buying options that a customer receives on the detail page, such as &#x60;B2B&#x60;, &#x60;Fresh&#x60;, and &#x60;Subscribe n Save&#x60;. &#x60;buyingOptionType&#x60; currently supports &#x60;NEW&#x60; as a value. | 
**segmented_featured_offers** | [**List[SegmentedFeaturedOffer]**](SegmentedFeaturedOffer.md) | A list of segmented featured offers for the current buying option type. A segment can be considered as a group of regional contexts that all have the same featured offer. A regional context is a combination of factors such as customer type, region, or postal code and buying option. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_buying_option import FeaturedBuyingOption

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedBuyingOption from a JSON string
featured_buying_option_instance = FeaturedBuyingOption.from_json(json)
# print the JSON string representation of the object
print(FeaturedBuyingOption.to_json())

# convert the object into a dict
featured_buying_option_dict = featured_buying_option_instance.to_dict()
# create an instance of FeaturedBuyingOption from a dict
featured_buying_option_from_dict = FeaturedBuyingOption.from_dict(featured_buying_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


