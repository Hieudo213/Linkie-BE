from enum import Enum

class InteractionType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    SUPERLIKE = "superlike"
