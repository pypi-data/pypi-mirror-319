# FeeDetail

The type of fee, fee amount, and other details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fee_type** | **str** | The type of fee charged to a seller. | 
**fee_amount** | [**MoneyType**](MoneyType.md) |  | 
**fee_promotion** | [**MoneyType**](MoneyType.md) |  | [optional] 
**tax_amount** | [**MoneyType**](MoneyType.md) |  | [optional] 
**final_fee** | [**MoneyType**](MoneyType.md) |  | 
**included_fee_detail_list** | [**List[IncludedFeeDetail]**](IncludedFeeDetail.md) | A list of other fees that contribute to a given fee. | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fee_detail import FeeDetail

# TODO update the JSON string below
json = "{}"
# create an instance of FeeDetail from a JSON string
fee_detail_instance = FeeDetail.from_json(json)
# print the JSON string representation of the object
print(FeeDetail.to_json())

# convert the object into a dict
fee_detail_dict = fee_detail_instance.to_dict()
# create an instance of FeeDetail from a dict
fee_detail_from_dict = FeeDetail.from_dict(fee_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


