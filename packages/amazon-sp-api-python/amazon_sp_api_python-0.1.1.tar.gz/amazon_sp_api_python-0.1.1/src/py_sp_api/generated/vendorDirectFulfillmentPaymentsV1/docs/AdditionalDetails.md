# AdditionalDetails

A field where the selling party can provide additional information for tax-related or any other purposes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the additional information provided by the selling party. | 
**detail** | **str** | The detail of the additional information provided by the selling party. | 
**language_code** | **str** | The language code of the additional information detail. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentPaymentsV1.models.additional_details import AdditionalDetails

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalDetails from a JSON string
additional_details_instance = AdditionalDetails.from_json(json)
# print the JSON string representation of the object
print(AdditionalDetails.to_json())

# convert the object into a dict
additional_details_dict = additional_details_instance.to_dict()
# create an instance of AdditionalDetails from a dict
additional_details_from_dict = AdditionalDetails.from_dict(additional_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


