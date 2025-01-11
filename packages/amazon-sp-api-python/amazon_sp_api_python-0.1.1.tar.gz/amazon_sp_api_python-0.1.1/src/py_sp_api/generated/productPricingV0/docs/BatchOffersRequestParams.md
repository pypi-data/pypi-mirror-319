# BatchOffersRequestParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which prices are returned. | 
**item_condition** | [**ItemCondition**](ItemCondition.md) |  | 
**customer_type** | [**CustomerType**](CustomerType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.batch_offers_request_params import BatchOffersRequestParams

# TODO update the JSON string below
json = "{}"
# create an instance of BatchOffersRequestParams from a JSON string
batch_offers_request_params_instance = BatchOffersRequestParams.from_json(json)
# print the JSON string representation of the object
print(BatchOffersRequestParams.to_json())

# convert the object into a dict
batch_offers_request_params_dict = batch_offers_request_params_instance.to_dict()
# create an instance of BatchOffersRequestParams from a dict
batch_offers_request_params_from_dict = BatchOffersRequestParams.from_dict(batch_offers_request_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


