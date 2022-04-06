from pathlib import Path
from typing import Any
from fastdoc import config


class ObjectType:
    def __init__(self, folder: Path, type: str = "", pics: list[str] = [], name: str = "Sem nome") -> None:
        self.folder: Path = folder
        self.type: str = type
        self.pics: list[str] = pics
        self.name: str = name

    def pics_iterator(self):
        for pic in self.pics:
            yield self.folder / pic

    def to_dict(self) -> dict[str, Any]:
        return {
            'folder': self.folder,
            'type': self.type,
            'pics': self.pics,
            'name': self.name
        }

    def from_dict(self, data: dict[str, Any]) -> 'ObjectType':
        self.folder = Path(data['folder'])
        self.type = data['type']
        self.name = data['name']
        self.pics = data['pics']
        return self



class CaseObjectsType:
    def __init__(
            self, folder: Path = config.workdir, objects: list[ObjectType] = [],
            pics_not_classified: list[str] = [],
            alias: str = "") -> None:
        self.folder: Path = folder
        self.objects: list[ObjectType] = objects
        self.pics_not_classified: list[str] = pics_not_classified
        self.alias: str = alias

    def pics_not_classified_iterator(self):
        for pic in self.pics_not_classified:
            yield self.folder / pic

    def to_dict(self) -> dict[str, Any]:
        return {
            'folder': self.folder,
            'objects': [obj.to_dict() for obj in self.objects],
            'pics_not_classified': self.pics_not_classified,
            'alias': self.alias
        }

    def from_dict(self, data: dict[str, Any]) -> 'CaseObjectsType':
        self.folder = Path(data['folder'])
        self.objects = [ObjectType(self.folder).from_dict(item) for item in data['objects']]
        self.pics_not_classified = data['pics_not_classified']
        self.alias = data['alias']
        return self

