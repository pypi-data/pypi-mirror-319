# FeesEstimateByIdRequest

A product, marketplace, and proposed price used to request estimated fees.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fees_estimate_request** | [**FeesEstimateRequest**](FeesEstimateRequest.md) |  | [optional] 
**id_type** | [**IdType**](IdType.md) |  | 
**id_value** | **str** | The item identifier. | 

## Example

```python
from py_sp_api.generated.productFeesV0.models.fees_estimate_by_id_request import FeesEstimateByIdRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FeesEstimateByIdRequest from a JSON string
fees_estimate_by_id_request_instance = FeesEstimateByIdRequest.from_json(json)
# print the JSON string representation of the object
print(FeesEstimateByIdRequest.to_json())

# convert the object into a dict
fees_estimate_by_id_request_dict = fees_estimate_by_id_request_instance.to_dict()
# create an instance of FeesEstimateByIdRequest from a dict
fees_estimate_by_id_request_from_dict = FeesEstimateByIdRequest.from_dict(fees_estimate_by_id_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


