# ListOfferMetricsResponseOffer

An object which contains offer metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number (ASIN). | [optional] 
**not_delivered_due_to_oos** | **float** | The percentage of items that were not shipped out of the total shipped units over a period of time due to being out of stock. Applicable to PERFORMANCE timePeriodType. | [optional] 
**total_subscriptions_revenue** | **float** | The revenue generated from subscriptions over a period of time. Applicable to PERFORMANCE timePeriodType. | [optional] 
**shipped_subscription_units** | **float** | The number of units shipped to the subscribers over a period of time. Applicable to PERFORMANCE timePeriodType. | [optional] 
**active_subscriptions** | **float** | The number of active subscriptions present at the end of the period. Applicable to PERFORMANCE timePeriodType. | [optional] 
**revenue_penetration** | **float** | The percentage of total program revenue out of total product revenue. Applicable to PERFORMANCE timePeriodType. | [optional] 
**lost_revenue_due_to_oos** | **float** | The revenue that would have been generated had there not been out of stock. Applicable to PERFORMANCE timePeriodType. | [optional] 
**coupons_revenue_penetration** | **float** | The percentage of revenue from ASINs with coupons out of total revenue from all ASINs. Applicable to PERFORMANCE timePeriodType. | [optional] 
**share_of_coupon_subscriptions** | **float** | The percentage of new subscriptions acquired through coupons. Applicable to PERFORMANCE timePeriodType. | [optional] 
**next30_day_total_subscriptions_revenue** | **float** | The forecasted total subscription revenue for the next 30 days. Applicable to FORECAST timePeriodType. | [optional] 
**next60_day_total_subscriptions_revenue** | **float** | The forecasted total subscription revenue for the next 60 days. Applicable to FORECAST timePeriodType. | [optional] 
**next90_day_total_subscriptions_revenue** | **float** | The forecasted total subscription revenue for the next 90 days. Applicable to FORECAST timePeriodType. | [optional] 
**next30_day_shipped_subscription_units** | **float** | The forecasted shipped subscription units for the next 30 days. Applicable to FORECAST timePeriodType. | [optional] 
**next60_day_shipped_subscription_units** | **float** | The forecasted shipped subscription units for the next 60 days. Applicable to FORECAST timePeriodType. | [optional] 
**next90_day_shipped_subscription_units** | **float** | The forecasted shipped subscription units for the next 90 days. Applicable to FORECAST timePeriodType. | [optional] 
**time_interval** | [**TimeInterval**](TimeInterval.md) |  | [optional] 
**currency_code** | **str** | The currency code in ISO 4217 format. | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.list_offer_metrics_response_offer import ListOfferMetricsResponseOffer

# TODO update the JSON string below
json = "{}"
# create an instance of ListOfferMetricsResponseOffer from a JSON string
list_offer_metrics_response_offer_instance = ListOfferMetricsResponseOffer.from_json(json)
# print the JSON string representation of the object
print(ListOfferMetricsResponseOffer.to_json())

# convert the object into a dict
list_offer_metrics_response_offer_dict = list_offer_metrics_response_offer_instance.to_dict()
# create an instance of ListOfferMetricsResponseOffer from a dict
list_offer_metrics_response_offer_from_dict = ListOfferMetricsResponseOffer.from_dict(list_offer_metrics_response_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


