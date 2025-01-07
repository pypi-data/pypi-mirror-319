from cq_studio.utils import Size

defaults = {
    "angular-tolerance": 0.01,
    "axes-colour": (1, 0, 0),
    "colour_quantization": 4,
    "excluded-dirs": [".venv", ".git"],
    "export-models": True,
    "linear-tolerance": 0.01,
    "listen-address": "127.0.0.1",
    "listen-port": 32323,
    "model-size": Size(200.0, 200.0, 100.0),
    "poll-interval": 1.0,
    "quiet": False,
    "show-axes-origin": True,
    "verbose": False,
}
