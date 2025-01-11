# Business

Information about the Seller's business. These fields may be omitted if the Seller is registered as an individual.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The registered business name. | 
**registered_business_address** | [**Address**](Address.md) |  | 
**company_registration_number** | **str** | The seller&#39;s company registration number, if applicable. This field will be absent for individual sellers and sole proprietorships. | [optional] 
**company_tax_identification_number** | **str** | The seller&#39;s company tax identification number, if applicable. This field will be present for certain business types only, such as sole proprietorships. | [optional] 
**non_latin_name** | **str** | The non-Latin script version of the registered business name, if applicable. | [optional] 

## Example

```python
from py_sp_api.generated.sellers.models.business import Business

# TODO update the JSON string below
json = "{}"
# create an instance of Business from a JSON string
business_instance = Business.from_json(json)
# print the JSON string representation of the object
print(Business.to_json())

# convert the object into a dict
business_dict = business_instance.to_dict()
# create an instance of Business from a dict
business_from_dict = Business.from_dict(business_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


