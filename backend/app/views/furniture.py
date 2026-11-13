from pydantic import BaseModel


class FurnitureView(BaseModel):
    id: str
    name: str
    category: str
    description: str
    color: str
    reference_alt: str
    photo_url: str
    is_demo: bool

    @classmethod
    def from_record(cls, item: dict):
        return cls(
            id=item["id"],
            name=item["name"],
            category=item["category"],
            description=item["description"],
            color=item["color"],
            reference_alt=f"{item['name']} — foto do móvel",
            photo_url=f"/media/{item['photo_path']}",
            is_demo=bool(item["is_demo"]),
        )
