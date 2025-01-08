import importlib
from pathlib import Path

from omnipy import (ConfigPersistOutputsOptions,
                    ConfigRestoreOutputsOptions,
                    EngineChoice,
                    PandasDataset,
                    runtime)
import typer

app = typer.Typer()


def get_path_to_example_data() -> Path:
    ref = importlib.resources.files('omnipy_example_data')
    path: Path
    with importlib.resources.as_file(ref) as path:
        return path.resolve()


installed_example_data_path = get_path_to_example_data()


@app.command()
def bed(
    owner: str = 'sunyumail93',
    repo: str = 'Bed12Processing',
    branch: str = 'master',
    path: str = 'data',
    file_suffix: str = 'bed12',
) -> PandasDataset:
    from omnipy_examples.bed import import_bed_files_to_pandas
    return import_bed_files_to_pandas.run(
        owner=owner, repo=repo, branch=branch, path=path, file_suffix=file_suffix)


@app.command()
def dagsim(input_dir: str = installed_example_data_path.joinpath('bif')) -> object:
    from omnipy_examples.dagsim import import_and_convert_bif_files_to_json
    return import_and_convert_bif_files_to_json.run(input_dir)


@app.command()
def encode() -> object:
    from omnipy_examples.encode import import_and_flatten_encode_data
    return import_and_flatten_encode_data.run()


@app.command()
def gff(input_dir: str = installed_example_data_path.joinpath('gff')) -> object:
    from omnipy_examples.gff import import_gff_as_pandas
    return import_gff_as_pandas.run(input_dir)


@app.command()
def isajson(input_dir: str = installed_example_data_path.joinpath('isa-json')) -> object:
    from omnipy_examples.isajson import convert_isa_json_to_relational_tables
    return convert_isa_json_to_relational_tables.run(input_dir)


@app.command()
def uniprot() -> object:
    from omnipy_examples.uniprot import import_and_flatten_uniprot_with_magic
    return import_and_flatten_uniprot_with_magic.run()


@app.command()
def chatgpt() -> object:
    from omnipy_examples.chatgpt import \
        get_chatgpt_interpretation_of_biorxiv_entries_and_commit_loop
    return get_chatgpt_interpretation_of_biorxiv_entries_and_commit_loop.run()


@app.callback()
def main(output_dir: str = runtime.config.job.output_storage.local.persist_data_dir_path,
         engine: EngineChoice = 'local',
         persist_outputs: ConfigPersistOutputsOptions = 'all',
         restore_outputs: ConfigRestoreOutputsOptions = 'disabled'):

    runtime.config.engine = engine
    runtime.config.job.output_storage.local.persist_data_dir_path = output_dir
    runtime.config.job.output_storage.persist_outputs = persist_outputs
    runtime.config.job.output_storage.restore_outputs = restore_outputs
    runtime.config.data.interactive_mode = True


if __name__ == '__main__':
    app()
