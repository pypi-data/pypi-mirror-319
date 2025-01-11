# FeesEstimate

The total estimated fees for an item and a list of details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_of_fees_estimation** | **datetime** | The time at which the fees were estimated. This defaults to the time the request is made. | 
**total_fees_estimate** | [**MoneyType**](MoneyType.md) |  | [optional] 
**fee_detail_list** | [**List[FeeDetail]**](FeeDetail.md) | A list of other fees that contribute to a given fee. | [optional] 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate import FeesEstimate

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimate from a JSON string
fees_estimate_instance = FeesEstimate.from_json(json)
# print the JSON string representation of the object
print(FeesEstimate.to_json())

# convert the object into a dict
fees_estimate_dict = fees_estimate_instance.to_dict()
# create an instance of FeesEstimate from a dict
fees_estimate_from_dict = FeesEstimate.from_dict(fees_estimate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


