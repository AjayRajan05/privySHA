from privysha.stages.optimizer import Optimizer


def test_optimizer_detects_analyze_dataset():

    optimizer = Optimizer()

    result = optimizer.run(
        "analyze this dataset for anomalies"
    )

    assert "@analyze(dataset)" in result


def test_optimizer_compression():

    optimizer = Optimizer()

    text = "analyze this dataset for anomalies and patterns in the data quickly"

    result = optimizer.run(text)

    assert len(result) > 0