# BuyerInfo

Buyer information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer_email** | **str** | The anonymized email address of the buyer. | [optional] 
**buyer_name** | **str** | The buyer name or the recipient name. | [optional] 
**buyer_county** | **str** | The county of the buyer.  **Note**: This attribute is only available in the Brazil marketplace. | [optional] 
**buyer_tax_info** | [**BuyerTaxInfo**](BuyerTaxInfo.md) |  | [optional] 
**purchase_order_number** | **str** | The purchase order (PO) number entered by the buyer at checkout. Only returned for orders where the buyer entered a PO number at checkout. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.buyer_info import BuyerInfo

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerInfo from a JSON string
buyer_info_instance = BuyerInfo.from_json(json)
# print the JSON string representation of the object
print(BuyerInfo.to_json())

# convert the object into a dict
buyer_info_dict = buyer_info_instance.to_dict()
# create an instance of BuyerInfo from a dict
buyer_info_from_dict = BuyerInfo.from_dict(buyer_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


