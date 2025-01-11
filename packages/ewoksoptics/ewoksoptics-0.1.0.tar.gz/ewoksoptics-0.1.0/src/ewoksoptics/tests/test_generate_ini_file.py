import os
import pytest

from ..tasks.generate_ini_file import GenerateIniFile


def _get_inputs(tmpdir, template: str) -> dict:
    return {
        "template_file": str(template),
        "mapping_data": {
            "___METHOD___": "xsvt",
            "___MAT___": "Al",
            "___SAMPLETAG___": "nr1121c",
            "___EEE___": 20.000001,
        },
        "output_file": tmpdir.join("result.ini"),
    }


def test_generate_ini_file(tmpdir):
    template = tmpdir.join("template.ini")
    template.write(
        """
    [SpeckleMPy]
    method = '___METHOD___'
    sample_tag = '___SAMPLETAG___'
    material = '___MAT___'
    delta = ''
    energy = ___EEE___
    pix_size = ___PIX___
    """
    )
    ini_inputs = _get_inputs(tmpdir, template)
    generate = GenerateIniFile(inputs=ini_inputs)
    generate.execute()
    output_ini_file = generate.get_output_value("output_file")
    assert os.path.exists(output_ini_file)
    with open(output_ini_file, "r") as f:
        content = f.read()
    expected_content = """
    [SpeckleMPy]
    method = 'xsvt'
    sample_tag = 'nr1121c'
    material = 'Al'
    delta = ''
    energy = 20.000001
    pix_size = ___PIX___
    """
    assert content.strip() == expected_content.strip()


def test_generate_ini_file_with_missing_template(tmpdir):
    template = tmpdir.join("non_existent_template.ini")
    assert not os.path.exists(template)
    ini_inputs = _get_inputs(tmpdir, template)
    task_name = f"{GenerateIniFile.__module__}.{GenerateIniFile.__name__}"
    generate = GenerateIniFile(inputs=ini_inputs)
    with pytest.raises(RuntimeError, match=f"Task '{task_name}' failed") as exc_info:
        generate.execute()
    original_exception = exc_info.value.__cause__
    assert isinstance(original_exception, FileNotFoundError)
    assert f"No such file or directory: '{template}'" in str(original_exception)
