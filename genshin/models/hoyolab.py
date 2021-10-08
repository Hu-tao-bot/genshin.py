from pydantic import BaseModel, Field


class GenshinAccount(BaseModel):
    uid: int = Field(alias="game_uid")
    level: int
    nickname: str
    server: str = Field(alias="region")
    server_name: str = Field(alias="region_name")

    # unknown meaning
    biz: str = Field(alias="game_biz")
    chosen: bool = Field(alias="is_chosen")
    official: bool = Field(alias="is_official")


class RecordCardData(BaseModel):
    name: str
    value: str


class RecordCard(BaseModel):
    uid: int = Field(alias="game_role_id")
    level: int
    nickname: str
    server: str = Field(alias="region")
    server_name: str = Field(alias="region_name")

    data: list[RecordCardData]

    # unknown meaning
    background_image: str
    has_uid: bool = Field(alias="has_role")
    public: bool = Field(alias="is_public")

    @property
    def days_active(self):
        return int(self.data[0].value)

    @property
    def characters(self):
        return int(self.data[1].value)

    @property
    def achievements(self):
        return int(self.data[2].value)

    @property
    def spiral_abyss(self):
        return self.data[3].value

    def as_dict(self, lang: str = "en-us"):
        """Helper function which turns fields into properly named ones"""
        assert lang == "en-us", "Other languages not yet implemented"

        return {d.name: (int(d.value) if d.value.isdigit() else d.value) for d in self.data}


class SearchUser(BaseModel):
    hoyolab_uid: int = Field(alias="uid")
    nickname: str
    introduction: str = Field(alias="introduce")
    avatar_id: int = Field(alias="avatar")
    gender: int
    icon: str = Field(alias="avatar_url")
