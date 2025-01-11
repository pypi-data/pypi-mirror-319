# ServiceFeeEvent

A service fee on the seller's account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**fee_reason** | **str** | A short description of the service fee reason. | [optional] 
**fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**seller_sku** | **str** | The seller SKU of the item. The seller SKU is qualified by the seller&#39;s seller ID, which is included with every call to the Selling Partner API. | [optional] 
**fn_sku** | **str** | A unique identifier assigned by Amazon to products stored in and fulfilled from an Amazon fulfillment center. | [optional] 
**fee_description** | **str** | A short description of the service fee event. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**store_name** | **str** | The name of the store where the event occurred. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.service_fee_event import ServiceFeeEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceFeeEvent from a JSON string
service_fee_event_instance = ServiceFeeEvent.from_json(json)
# print the JSON string representation of the object
print(ServiceFeeEvent.to_json())

# convert the object into a dict
service_fee_event_dict = service_fee_event_instance.to_dict()
# create an instance of ServiceFeeEvent from a dict
service_fee_event_from_dict = ServiceFeeEvent.from_dict(service_fee_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


