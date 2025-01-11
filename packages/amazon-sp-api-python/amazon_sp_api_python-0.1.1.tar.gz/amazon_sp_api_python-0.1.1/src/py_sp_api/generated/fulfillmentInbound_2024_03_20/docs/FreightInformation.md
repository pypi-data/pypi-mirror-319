# FreightInformation

Freight information describes the skus being transported. Freight carrier options and quotes will only be returned if the freight information is provided.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**declared_value** | [**Currency**](Currency.md) |  | [optional] 
**freight_class** | **str** | Freight class.  Possible values: &#x60;NONE&#x60;, &#x60;FC_50&#x60;, &#x60;FC_55&#x60;, &#x60;FC_60&#x60;, &#x60;FC_65&#x60;, &#x60;FC_70&#x60;, &#x60;FC_77_5&#x60;, &#x60;FC_85&#x60;, &#x60;FC_92_5&#x60;, &#x60;FC_100&#x60;, &#x60;FC_110&#x60;, &#x60;FC_125&#x60;, &#x60;FC_150&#x60;, &#x60;FC_175&#x60;, &#x60;FC_200&#x60;, &#x60;FC_250&#x60;, &#x60;FC_300&#x60;, &#x60;FC_400&#x60;, &#x60;FC_500&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.freight_information import FreightInformation

# TODO update the JSON string below
json = "{}"
# create an instance of FreightInformation from a JSON string
freight_information_instance = FreightInformation.from_json(json)
# print the JSON string representation of the object
print(FreightInformation.to_json())

# convert the object into a dict
freight_information_dict = freight_information_instance.to_dict()
# create an instance of FreightInformation from a dict
freight_information_from_dict = FreightInformation.from_dict(freight_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


