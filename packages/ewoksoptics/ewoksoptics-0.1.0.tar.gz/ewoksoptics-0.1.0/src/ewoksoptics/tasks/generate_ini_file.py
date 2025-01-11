from ewokscore import Task


class GenerateIniFile(
    Task,
    input_names=[
        "template_file",
        "mapping_data",
        "output_file",
    ],
    output_names=[
        "output_file",
    ],
):
    """
    Generate the ini file needed for the detector distorsion.
    Save it in output_file.
    Inputs:
        - template_file: string, path of the ini template file
        - mapping_data: dict[str, any],
            A dictionary of key-value pairs used for substitution in the template file
        - output_file: string,
            the full path (including filename) where the ini file will be saved
    Outputs:
        - output_file: string,
            the full path (including filename) where the ini file is saved
    """

    def run(self):
        with open(self.inputs.template_file, "r") as template:
            template_content = template.read()
        filled_content = template_content
        for key, value in self.inputs.mapping_data.items():
            filled_content = filled_content.replace(key, str(value))
        with open(self.inputs.output_file, "w") as f:
            f.write(filled_content)
        self.outputs.output_file = self.inputs.output_file
