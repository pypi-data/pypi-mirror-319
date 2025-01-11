# IncludedFeeDetail

The type of fee, fee amount, and other details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fee_type** | **str** | The type of fee charged to a seller. | 
**fee_amount** | [**MoneyType**](MoneyType.md) |  | 
**fee_promotion** | [**MoneyType**](MoneyType.md) |  | [optional] 
**tax_amount** | [**MoneyType**](MoneyType.md) |  | [optional] 
**final_fee** | [**MoneyType**](MoneyType.md) |  | 

## Example

```python
from py_sp_api.generated.productFeesV0.models.included_fee_detail import IncludedFeeDetail

# TODO update the JSON string below
json = "{}"
# create an instance of IncludedFeeDetail from a JSON string
included_fee_detail_instance = IncludedFeeDetail.from_json(json)
# print the JSON string representation of the object
print(IncludedFeeDetail.to_json())

# convert the object into a dict
included_fee_detail_dict = included_fee_detail_instance.to_dict()
# create an instance of IncludedFeeDetail from a dict
included_fee_detail_from_dict = IncludedFeeDetail.from_dict(included_fee_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


