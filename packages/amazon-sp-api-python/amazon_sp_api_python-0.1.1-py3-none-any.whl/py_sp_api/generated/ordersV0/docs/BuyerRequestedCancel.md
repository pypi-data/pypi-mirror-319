# BuyerRequestedCancel

Information about whether or not a buyer requested cancellation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_buyer_requested_cancel** | **str** | Indicate whether the buyer has requested cancellation.  **Possible Values**: &#x60;true&#x60;, &#x60;false&#x60;. | [optional] 
**buyer_cancel_reason** | **str** | The reason that the buyer requested cancellation. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.buyer_requested_cancel import BuyerRequestedCancel

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerRequestedCancel from a JSON string
buyer_requested_cancel_instance = BuyerRequestedCancel.from_json(json)
# print the JSON string representation of the object
print(BuyerRequestedCancel.to_json())

# convert the object into a dict
buyer_requested_cancel_dict = buyer_requested_cancel_instance.to_dict()
# create an instance of BuyerRequestedCancel from a dict
buyer_requested_cancel_from_dict = BuyerRequestedCancel.from_dict(buyer_requested_cancel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


