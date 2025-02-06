from pydantic import BaseModel
from typing import Optional


class Exercise(BaseModel):
    id: int
    partiesid: int
    name: str
    image: Optional[bytes] = (
        "https://www.fabrykasily.pl/upload/gallery/2018/07/id_18973_1532436684_1260x841.jpg"
    )
    hardrate: Optional[str]
    description: Optional[str]
    serieshint: Optional[int]
    counthint: Optional[int]
    breakhint: Optional[int]
    position: str = "Połóż się na ławce, stopy stabilnie na ziemi, plecy lekko wygięte."
    performing: str = (
        "Chwyć sztangę na szerokość barków, opuść ją powoli do klatki piersiowej, a następnie dynamicznie wypchnij do góry."
    )
    tips: str = (
        "Nie blokuj łokci na górze, kontroluj ruch, nie odbijaj sztangi od klatki."
    )
