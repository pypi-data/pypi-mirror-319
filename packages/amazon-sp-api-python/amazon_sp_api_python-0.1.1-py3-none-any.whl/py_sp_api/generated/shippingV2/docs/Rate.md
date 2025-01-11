# Rate

The details of a shipping service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rate_id** | **str** | An identifier for the rate (shipment offering) provided by a shipping service provider. | 
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | 
**carrier_name** | **str** | The carrier name for the offering. | 
**service_id** | **str** | An identifier for the shipping service. | 
**service_name** | **str** | The name of the shipping service. | 
**billed_weight** | [**Weight**](Weight.md) |  | [optional] 
**total_charge** | [**Currency**](Currency.md) |  | 
**promise** | [**Promise**](Promise.md) |  | 
**supported_document_specifications** | [**List[SupportedDocumentSpecification]**](SupportedDocumentSpecification.md) | A list of the document specifications supported for a shipment service offering. | 
**available_value_added_service_groups** | [**List[AvailableValueAddedServiceGroup]**](AvailableValueAddedServiceGroup.md) | A list of value-added services available for a shipping service offering. | [optional] 
**requires_additional_inputs** | **bool** | When true, indicates that additional inputs are required to purchase this shipment service. You must then call the getAdditionalInputs operation to return the JSON schema to use when providing the additional inputs to the purchaseShipment operation. | 
**rate_item_list** | [**List[RateItem]**](RateItem.md) | A list of RateItem | [optional] 
**payment_type** | [**PaymentType**](PaymentType.md) |  | [optional] 
**benefits** | [**Benefits**](Benefits.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.rate import Rate

# TODO update the JSON string below
json = "{}"
# create an instance of Rate from a JSON string
rate_instance = Rate.from_json(json)
# print the JSON string representation of the object
print(Rate.to_json())

# convert the object into a dict
rate_dict = rate_instance.to_dict()
# create an instance of Rate from a dict
rate_from_dict = Rate.from_dict(rate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


