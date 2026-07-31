"""Smoke tests for Flask, Django, and LlamaIndex integrations."""

import pytest


def test_flask_middleware_import_and_request():
    pytest.importorskip("flask")
    from flask import Flask

    from asha.integrations.flask.middleware import ASHAMiddleware

    app = Flask(__name__)
    ASHAMiddleware(app, endpoints=["/api/chat"], privacy=True)

    @app.route("/api/chat", methods=["POST"])
    def chat():
        return {"ok": True}

    client = app.test_client()
    response = client.post(
        "/api/chat",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )
    assert response.status_code == 200


def test_django_middleware_import():
    pytest.importorskip("django")
    from asha.integrations.django.middleware import ASHAMiddleware

    assert callable(ASHAMiddleware)
    assert hasattr(ASHAMiddleware, "_should_process_endpoint") or hasattr(
        ASHAMiddleware, "__init__"
    )


def test_llamaindex_plugin_import():
    llama = pytest.importorskip("llama_index.core")
    assert llama is not None
    from asha.integrations.llamaindex.plugin import wrap_query_engine

    class _MockQE:
        def query(self, bundle):
            return f"ok:{getattr(bundle, 'query_str', bundle)}"

    wrapped = wrap_query_engine(_MockQE(), privacy=False)
    assert type(wrapped).__name__ == "ASHAQueryEngine"
