# PrepInstruction

Information pertaining to the preparation of inbound goods.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fee** | [**Currency**](Currency.md) |  | [optional] 
**prep_owner** | **str** | In some situations, special preparations are required for items and this field reflects the owner of the preparations. Options include &#x60;AMAZON&#x60;, &#x60;SELLER&#x60; or &#x60;NONE&#x60;. | [optional] 
**prep_type** | **str** | Type of preparation that should be done.  Possible values: &#x60;ITEM_LABELING&#x60;, &#x60;ITEM_BUBBLEWRAP&#x60;, &#x60;ITEM_POLYBAGGING&#x60;, &#x60;ITEM_TAPING&#x60;, &#x60;ITEM_BLACK_SHRINKWRAP&#x60;, &#x60;ITEM_HANG_GARMENT&#x60;, &#x60;ITEM_BOXING&#x60;, &#x60;ITEM_SETCREAT&#x60;, &#x60;ITEM_RMOVHANG&#x60;, &#x60;ITEM_SUFFOSTK&#x60;, &#x60;ITEM_CAP_SEALING&#x60;, &#x60;ITEM_DEBUNDLE&#x60;, &#x60;ITEM_SETSTK&#x60;, &#x60;ITEM_SIOC&#x60;, &#x60;ITEM_NO_PREP&#x60;, &#x60;ADULT&#x60;, &#x60;BABY&#x60;, &#x60;TEXTILE&#x60;, &#x60;HANGER&#x60;, &#x60;FRAGILE&#x60;, &#x60;LIQUID&#x60;, &#x60;SHARP&#x60;, &#x60;SMALL&#x60;, &#x60;PERFORATED&#x60;, &#x60;GRANULAR&#x60;, &#x60;SET&#x60;, &#x60;FC_PROVIDED&#x60;, &#x60;UNKNOWN&#x60;, &#x60;NONE&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.prep_instruction import PrepInstruction

# TODO update the JSON string below
json = "{}"
# create an instance of PrepInstruction from a JSON string
prep_instruction_instance = PrepInstruction.from_json(json)
# print the JSON string representation of the object
print(PrepInstruction.to_json())

# convert the object into a dict
prep_instruction_dict = prep_instruction_instance.to_dict()
# create an instance of PrepInstruction from a dict
prep_instruction_from_dict = PrepInstruction.from_dict(prep_instruction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


