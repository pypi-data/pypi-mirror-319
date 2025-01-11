# InboundPackages

Represents the packages to inbound.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packages_to_inbound** | [**List[DistributionPackageQuantity]**](DistributionPackageQuantity.md) | List of packages to be inbounded. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inbound_packages import InboundPackages

# TODO update the JSON string below
json = "{}"
# create an instance of InboundPackages from a JSON string
inbound_packages_instance = InboundPackages.from_json(json)
# print the JSON string representation of the object
print(InboundPackages.to_json())

# convert the object into a dict
inbound_packages_dict = inbound_packages_instance.to_dict()
# create an instance of InboundPackages from a dict
inbound_packages_from_dict = InboundPackages.from_dict(inbound_packages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


