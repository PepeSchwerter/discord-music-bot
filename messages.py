import random

songs_comments = [
    "buen tema manito",
    "que buen tema manito",
    "tema malardo manito",
    "que temardo manito",
    "ponte algo bueno pa la otra manito",
    "que es esta wea manito?",
    "que temazo manito",
    "buena cancion manito"
]

def get_comment():
    return random.choice(songs_comments)