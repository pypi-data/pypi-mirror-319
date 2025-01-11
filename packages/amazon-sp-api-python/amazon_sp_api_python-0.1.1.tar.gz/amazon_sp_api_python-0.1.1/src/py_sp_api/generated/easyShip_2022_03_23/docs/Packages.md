# Packages

A list of packages.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packages** | [**List[Package]**](Package.md) | A list of packages. | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.packages import Packages

# TODO update the JSON string below
json = "{}"
# create an instance of Packages from a JSON string
packages_instance = Packages.from_json(json)
# print the JSON string representation of the object
print(Packages.to_json())

# convert the object into a dict
packages_dict = packages_instance.to_dict()
# create an instance of Packages from a dict
packages_from_dict = Packages.from_dict(packages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


