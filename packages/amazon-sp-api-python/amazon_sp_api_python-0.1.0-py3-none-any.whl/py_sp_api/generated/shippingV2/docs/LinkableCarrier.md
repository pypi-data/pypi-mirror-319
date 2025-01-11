# LinkableCarrier

Info About Linkable Carrier

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | [optional] 
**linkable_account_types** | [**List[LinkableAccountType]**](LinkableAccountType.md) | A list of LinkableAccountType | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.linkable_carrier import LinkableCarrier

# TODO update the JSON string below
json = "{}"
# create an instance of LinkableCarrier from a JSON string
linkable_carrier_instance = LinkableCarrier.from_json(json)
# print the JSON string representation of the object
print(LinkableCarrier.to_json())

# convert the object into a dict
linkable_carrier_dict = linkable_carrier_instance.to_dict()
# create an instance of LinkableCarrier from a dict
linkable_carrier_from_dict = LinkableCarrier.from_dict(linkable_carrier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


