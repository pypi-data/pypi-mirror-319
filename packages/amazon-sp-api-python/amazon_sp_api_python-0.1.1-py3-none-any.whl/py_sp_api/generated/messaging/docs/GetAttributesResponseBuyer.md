# GetAttributesResponseBuyer

The list of attributes related to the buyer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locale** | **str** | The buyer&#39;s language of preference, indicated with a locale-specific language tag. Examples: \&quot;en-US\&quot;, \&quot;zh-CN\&quot;, and \&quot;en-GB\&quot;. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.get_attributes_response_buyer import GetAttributesResponseBuyer

# TODO update the JSON string below
json = "{}"
# create an instance of GetAttributesResponseBuyer from a JSON string
get_attributes_response_buyer_instance = GetAttributesResponseBuyer.from_json(json)
# print the JSON string representation of the object
print(GetAttributesResponseBuyer.to_json())

# convert the object into a dict
get_attributes_response_buyer_dict = get_attributes_response_buyer_instance.to_dict()
# create an instance of GetAttributesResponseBuyer from a dict
get_attributes_response_buyer_from_dict = GetAttributesResponseBuyer.from_dict(get_attributes_response_buyer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


