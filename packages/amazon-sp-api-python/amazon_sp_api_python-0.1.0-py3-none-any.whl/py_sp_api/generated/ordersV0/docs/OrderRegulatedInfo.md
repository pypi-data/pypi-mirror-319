# OrderRegulatedInfo

The order's regulated information along with its verification status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier, in 3-7-7 format. | 
**regulated_information** | [**RegulatedInformation**](RegulatedInformation.md) |  | 
**requires_dosage_label** | **bool** | When true, the order requires attaching a dosage information label when shipped. | 
**regulated_order_verification_status** | [**RegulatedOrderVerificationStatus**](RegulatedOrderVerificationStatus.md) |  | 

## Example

```python
from py_sp_api.generated.ordersV0.models.order_regulated_info import OrderRegulatedInfo

# TODO update the JSON string below
json = "{}"
# create an instance of OrderRegulatedInfo from a JSON string
order_regulated_info_instance = OrderRegulatedInfo.from_json(json)
# print the JSON string representation of the object
print(OrderRegulatedInfo.to_json())

# convert the object into a dict
order_regulated_info_dict = order_regulated_info_instance.to_dict()
# create an instance of OrderRegulatedInfo from a dict
order_regulated_info_from_dict = OrderRegulatedInfo.from_dict(order_regulated_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


