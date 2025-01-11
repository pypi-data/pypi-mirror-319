# LinkObject

A Link object.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**href** | **str** | A URI for this object. | 
**name** | **str** | An identifier for this object. | [optional] 

## Example

```python
from py_sp_api.generated.solicitations.models.link_object import LinkObject

# TODO update the JSON string below
json = "{}"
# create an instance of LinkObject from a JSON string
link_object_instance = LinkObject.from_json(json)
# print the JSON string representation of the object
print(LinkObject.to_json())

# convert the object into a dict
link_object_dict = link_object_instance.to_dict()
# create an instance of LinkObject from a dict
link_object_from_dict = LinkObject.from_dict(link_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


