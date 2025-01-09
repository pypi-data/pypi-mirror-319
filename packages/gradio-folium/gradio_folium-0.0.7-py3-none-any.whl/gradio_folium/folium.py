from __future__ import annotations

from typing import Any, Callable
from gradio.components.base import Component
from folium import Map
from gradio.data_classes import FileData
from tempfile import NamedTemporaryFile


class Folium(Component):
    data_model = FileData

    def __init__(
        self,
        value: Any = None,
        *,
        height: int | None = None,
        label: str | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        load_fn: Callable[..., Any] | None = None,
        every: float | None = None,
    ):
        super().__init__(
            value,
            label=label,
            info=None,
            show_label=True,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            load_fn=load_fn,
            every=every,
        )
        self.height = height

    def preprocess(self, payload):
        return payload

    def postprocess(self, value: Map):
        if not value:
            return None
        with NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            value.save(tmp.name)
            return FileData(path=tmp.name)

    def example_inputs(self):
        return {"info": "Do not use as input"}

    def api_info(self):
        return {"type": {}, "description": "any valid json"}
