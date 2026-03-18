from privysha.pipeline import Pipeline


def test_pipeline_execution():

    pipeline = Pipeline()

    result = pipeline.process(
        "Hey bro analyze this dataset"
    )

    assert "compiled_prompt" in result
    assert "sanitized" in result