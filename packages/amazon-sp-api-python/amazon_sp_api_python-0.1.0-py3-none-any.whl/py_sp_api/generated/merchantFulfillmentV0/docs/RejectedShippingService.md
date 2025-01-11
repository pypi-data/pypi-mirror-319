# RejectedShippingService

Information about a rejected shipping service

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The rejected shipping carrier name. For example, USPS. | 
**shipping_service_name** | **str** | The rejected shipping service localized name. For example, FedEx Standard Overnight. | 
**shipping_service_id** | **str** | An Amazon-defined shipping service identifier. | 
**rejection_reason_code** | **str** | A reason code meant to be consumed programatically. For example, &#x60;CARRIER_CANNOT_SHIP_TO_POBOX&#x60;. | 
**rejection_reason_message** | **str** | A localized human readable description of the rejected reason. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.rejected_shipping_service import RejectedShippingService

# TODO update the JSON string below
json = "{}"
# create an instance of RejectedShippingService from a JSON string
rejected_shipping_service_instance = RejectedShippingService.from_json(json)
# print the JSON string representation of the object
print(RejectedShippingService.to_json())

# convert the object into a dict
rejected_shipping_service_dict = rejected_shipping_service_instance.to_dict()
# create an instance of RejectedShippingService from a dict
rejected_shipping_service_from_dict = RejectedShippingService.from_dict(rejected_shipping_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


