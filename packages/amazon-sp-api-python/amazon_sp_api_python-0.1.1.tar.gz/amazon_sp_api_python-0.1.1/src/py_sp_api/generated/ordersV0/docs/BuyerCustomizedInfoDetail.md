# BuyerCustomizedInfoDetail

Buyer information for custom orders from the Amazon Custom program.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customized_url** | **str** | The location of a ZIP file containing Amazon Custom data. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.buyer_customized_info_detail import BuyerCustomizedInfoDetail

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerCustomizedInfoDetail from a JSON string
buyer_customized_info_detail_instance = BuyerCustomizedInfoDetail.from_json(json)
# print the JSON string representation of the object
print(BuyerCustomizedInfoDetail.to_json())

# convert the object into a dict
buyer_customized_info_detail_dict = buyer_customized_info_detail_instance.to_dict()
# create an instance of BuyerCustomizedInfoDetail from a dict
buyer_customized_info_detail_from_dict = BuyerCustomizedInfoDetail.from_dict(buyer_customized_info_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


