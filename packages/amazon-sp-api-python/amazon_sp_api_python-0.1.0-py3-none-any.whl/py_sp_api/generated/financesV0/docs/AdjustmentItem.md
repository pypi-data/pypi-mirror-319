# AdjustmentItem

An item in an adjustment to the seller's account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quantity** | **str** | Represents the number of units in the seller&#39;s inventory when the AdustmentType is FBAInventoryReimbursement. | [optional] 
**per_unit_amount** | [**Currency**](Currency.md) |  | [optional] 
**total_amount** | [**Currency**](Currency.md) |  | [optional] 
**seller_sku** | **str** | The seller SKU of the item. The seller SKU is qualified by the seller&#39;s seller ID, which is included with every call to the Selling Partner API. | [optional] 
**fn_sku** | **str** | A unique identifier assigned to products stored in and fulfilled from a fulfillment center. | [optional] 
**product_description** | **str** | A short description of the item. | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**transaction_number** | **str** | The transaction number that is related to the adjustment. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.adjustment_item import AdjustmentItem

# TODO update the JSON string below
json = "{}"
# create an instance of AdjustmentItem from a JSON string
adjustment_item_instance = AdjustmentItem.from_json(json)
# print the JSON string representation of the object
print(AdjustmentItem.to_json())

# convert the object into a dict
adjustment_item_dict = adjustment_item_instance.to_dict()
# create an instance of AdjustmentItem from a dict
adjustment_item_from_dict = AdjustmentItem.from_dict(adjustment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


