from omnipy import (convert_dataset_list_of_dicts_to_pandas,
                    flatten_nested_json,
                    LinearFlowTemplate,
                    PandasDataset,
                    remove_columns)
from omnipy.components._fairtracks.tasks import import_dataset_from_encode

# cast_to_dict_on_top = cast_dataset.refine(
#     name='cast_to_dict_on_top',
#     fixed_params=dict(cast_model=JsonDictOfAnyModel),
# )

# encode_json_pruned =
# encode_json_dict = cast_to_dict_on_top.run(encode_json)

# runtime.config.engine = 'prefect'
# runtime.config.prefect.use_cached_results = True
#
#
# @FuncFlowTemplate()
# def import_encode_data_tmpl():
#     encode_json = import_dataset_from_encode(
#         endpoints=[
#             'experiment',
#             'biosample',
#         ],
#         max_data_item_count=25,
#         serialize_as='csv',
#     )
#     encode_json_pruned = remove_columns(
#         encode_json,
#         column_keys_for_data_items=dict(
#             experiment=['audit'],
#             biosample=['audit'],
#         ),
#         serialize_as='csv',
#     )
#     return encode_json_pruned
#
#
# import_encode_data.run()


@LinearFlowTemplate(
    import_dataset_from_encode.refine(
        fixed_params=dict(
            endpoints=[
                'experiment',
                'biosample',
            ],
            max_data_item_count=25,
        )),
    flatten_nested_json,
    remove_columns.refine(
        fixed_params=dict(
            column_keys_for_data_items=dict(
                experiment=['audit'],
                biosample=['audit'],
            ))),
    convert_dataset_list_of_dicts_to_pandas,
)
def import_and_flatten_encode_data() -> PandasDataset:
    ...
