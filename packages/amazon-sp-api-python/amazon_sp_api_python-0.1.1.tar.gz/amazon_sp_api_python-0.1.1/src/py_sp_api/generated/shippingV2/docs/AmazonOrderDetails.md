# AmazonOrderDetails

Amazon order information. This is required if the shipment source channel is Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **str** | The Amazon order ID associated with the Amazon order fulfilled by this shipment. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.amazon_order_details import AmazonOrderDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AmazonOrderDetails from a JSON string
amazon_order_details_instance = AmazonOrderDetails.from_json(json)
# print the JSON string representation of the object
print(AmazonOrderDetails.to_json())

# convert the object into a dict
amazon_order_details_dict = amazon_order_details_instance.to_dict()
# create an instance of AmazonOrderDetails from a dict
amazon_order_details_from_dict = AmazonOrderDetails.from_dict(amazon_order_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


