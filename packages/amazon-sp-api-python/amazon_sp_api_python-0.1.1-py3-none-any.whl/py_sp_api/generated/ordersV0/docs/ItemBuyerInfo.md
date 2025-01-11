# ItemBuyerInfo

A single item's buyer information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer_customized_info** | [**BuyerCustomizedInfoDetail**](BuyerCustomizedInfoDetail.md) |  | [optional] 
**gift_wrap_price** | [**Money**](Money.md) |  | [optional] 
**gift_wrap_tax** | [**Money**](Money.md) |  | [optional] 
**gift_message_text** | **str** | A gift message provided by the buyer.  **Note**: This attribute is only available for MFN (fulfilled by seller) orders. | [optional] 
**gift_wrap_level** | **str** | The gift wrap level specified by the buyer. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.item_buyer_info import ItemBuyerInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ItemBuyerInfo from a JSON string
item_buyer_info_instance = ItemBuyerInfo.from_json(json)
# print the JSON string representation of the object
print(ItemBuyerInfo.to_json())

# convert the object into a dict
item_buyer_info_dict = item_buyer_info_instance.to_dict()
# create an instance of ItemBuyerInfo from a dict
item_buyer_info_from_dict = ItemBuyerInfo.from_dict(item_buyer_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


