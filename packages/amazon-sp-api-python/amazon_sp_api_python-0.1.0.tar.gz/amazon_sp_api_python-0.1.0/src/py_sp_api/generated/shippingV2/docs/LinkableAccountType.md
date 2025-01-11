# LinkableAccountType

Info About Linkable Account Type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_type** | [**AccountType**](AccountType.md) |  | [optional] 
**carrier_account_inputs** | [**List[CarrierAccountInput]**](CarrierAccountInput.md) | A list of CarrierAccountInput | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.linkable_account_type import LinkableAccountType

# TODO update the JSON string below
json = "{}"
# create an instance of LinkableAccountType from a JSON string
linkable_account_type_instance = LinkableAccountType.from_json(json)
# print the JSON string representation of the object
print(LinkableAccountType.to_json())

# convert the object into a dict
linkable_account_type_dict = linkable_account_type_instance.to_dict()
# create an instance of LinkableAccountType from a dict
linkable_account_type_from_dict = LinkableAccountType.from_dict(linkable_account_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


