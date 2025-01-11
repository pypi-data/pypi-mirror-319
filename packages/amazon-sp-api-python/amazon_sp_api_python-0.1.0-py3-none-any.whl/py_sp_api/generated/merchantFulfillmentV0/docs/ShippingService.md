# ShippingService

A shipping service offer made by a carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_service_name** | **str** | A plain text representation of a carrier&#39;s shipping service. For example, \&quot;UPS Ground\&quot; or \&quot;FedEx Standard Overnight\&quot;.  | 
**carrier_name** | **str** | The name of the carrier. | 
**shipping_service_id** | **str** | An Amazon-defined shipping service identifier. | 
**shipping_service_offer_id** | **str** | An Amazon-defined shipping service offer identifier. | 
**ship_date** | **datetime** | Date-time formatted timestamp. | 
**earliest_estimated_delivery_date** | **datetime** | Date-time formatted timestamp. | [optional] 
**latest_estimated_delivery_date** | **datetime** | Date-time formatted timestamp. | [optional] 
**rate** | [**CurrencyAmount**](CurrencyAmount.md) |  | 
**shipping_service_options** | [**ShippingServiceOptions**](ShippingServiceOptions.md) |  | 
**available_shipping_service_options** | [**AvailableShippingServiceOptions**](AvailableShippingServiceOptions.md) |  | [optional] 
**available_label_formats** | [**List[LabelFormat]**](LabelFormat.md) | List of label formats. | [optional] 
**available_format_options_for_label** | [**List[LabelFormatOption]**](LabelFormatOption.md) | The available label formats. | [optional] 
**requires_additional_seller_inputs** | **bool** | When true, additional seller inputs are required. | 
**benefits** | [**Benefits**](Benefits.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.shipping_service import ShippingService

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingService from a JSON string
shipping_service_instance = ShippingService.from_json(json)
# print the JSON string representation of the object
print(ShippingService.to_json())

# convert the object into a dict
shipping_service_dict = shipping_service_instance.to_dict()
# create an instance of ShippingService from a dict
shipping_service_from_dict = ShippingService.from_dict(shipping_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


