from scoper.variables import VariableProcessor


def test_variable_processor_basic():
    vars = {"project_name": "Test Project"}
    processor = VariableProcessor(vars)
    content = "Hello {{project_name}}"
    assert processor.process(content) == "Hello Test Project"


def test_variable_processor_builtin():
    processor = VariableProcessor()
    content = "{{year}}"
    import datetime
    assert processor.process(content) == str(datetime.datetime.now().year)


def test_variable_processor_jinja2():
    vars = {"items": ["a", "b", "c"]}
    processor = VariableProcessor(vars)
    content = "{% for item in items %}{{item}}{% endfor %}"
    result = processor.process_jinja2(content)
    assert result == "abc"
