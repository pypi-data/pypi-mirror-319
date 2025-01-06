"""A generator used to generate C++ based on a schema."""

from logging import Logger
from pathlib import Path
import jinja2
from cmg.templates import (
    cmakelists_txt_j2,
    klass_cpp_j2,
    test_cpp_j2,
    identifiable_hpp_j2,
    identifiable_cpp_j2,
    index_hpp_j2,
    index_cpp_j2,
    persistable_hpp_j2,
    persistence_hpp_j2,
)
import cmg.templates.klass_hpp_j2 as klass_hpp_j2
from cmg.schema import Schema, Klass, Field
from importlib.machinery import SourceFileLoader

from cmg.validation import SchemaRuleSet


def schema_loader(schema: str) -> Schema:
    """Load the schema module."""

    module = SourceFileLoader("schema", schema).load_module()
    return module.schema


def generate(schema: Schema, output_dir: str, logger: Logger) -> int:
    """Generate C++ code based on the schema."""

    logger.info("Validating schema ...")
    errors = SchemaRuleSet().validate(schema)

    if len(errors) > 0:
        for error in errors:
            logger.error(error.message)
        return 1

    logger.info("Generating code ...")

    # Create the directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Link the schema
    schema.link()
    schema.set_output_dir(output_dir)

    # Build the C++ code

    # Templates
    hpp_template = jinja2.Template(klass_hpp_j2.TEMPLATE)
    cpp_template = jinja2.Template(klass_cpp_j2.TEMPLATE)
    supplementary_templates = {
        "identifiable.hpp": jinja2.Template(identifiable_hpp_j2.TEMPLATE),
        "identifiable.cpp": jinja2.Template(identifiable_cpp_j2.TEMPLATE),
        "index.hpp": jinja2.Template(index_hpp_j2.TEMPLATE),
        "index.cpp": jinja2.Template(index_cpp_j2.TEMPLATE),
        "persistable.hpp": jinja2.Template(persistable_hpp_j2.TEMPLATE),
        "persistence.hpp": jinja2.Template(persistence_hpp_j2.TEMPLATE),
    }
    cmakelists_template = jinja2.Template(cmakelists_txt_j2.TEMPLATE)
    test_template = jinja2.Template(test_cpp_j2.TEMPLATE)

    for klass in schema.classes:
        hpp_file = f"{output_dir}/{klass.to_snake_case()}.hpp"
        with open(hpp_file, "w") as f:
            f.write(hpp_template.render(schema=schema, klass=klass))
        cpp_file = f"{output_dir}/{klass.to_snake_case()}.cpp"
        with open(cpp_file, "w") as f:
            f.write(cpp_template.render(schema=schema, klass=klass))

    supplementary_classes = [
        "identifiable",
        "index",
    ]
    for klass in supplementary_classes:
        header_file = f"{output_dir}/{klass}.hpp"
        with open(header_file, "w") as f:
            f.write(supplementary_templates[f"{klass}.hpp"].render(schema=schema))
        cpp_file = f"{output_dir}/{klass}.cpp"
        with open(cpp_file, "w") as f:
            f.write(supplementary_templates[f"{klass}.cpp"].render(schema=schema))

    header_only_classes = ["persistable", "persistence"]
    for klass in header_only_classes:
        header_file = f"{output_dir}/{klass}.hpp"
        with open(header_file, "w") as f:
            f.write(supplementary_templates[f"{klass}.hpp"].render(schema=schema))

    cmakelists_file = f"{output_dir}/CMakeLists.txt"
    with open(cmakelists_file, "w") as f:
        f.write(cmakelists_template.render(schema=schema))

    test_file = f"{output_dir}/test_{schema.namespace}.cpp"
    with open(test_file, "w") as f:
        f.write(test_template.render(schema=schema))

    return 0
