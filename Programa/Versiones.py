import sys, importlib

pkgs = [
    "PySide6",
    "sounddevice",
    "google.cloud.speech",
    "spacy",
    "unidecode",
    "pymycobot",
]

def get_version(modname):
    try:
        m = importlib.import_module(modname)
        return getattr(m, "__version__", None)
    except Exception:
        return None

print("Python:", sys.version.split()[0])
for name in pkgs:
    ver = get_version(name)
    # google.cloud.speech no expone __version__ directamente:
    if ver is None and name == "google.cloud.speech":
        try:
            import importlib.metadata as md
            ver = md.version("google-cloud-speech")
        except Exception:
            ver = "desconocida"
    print(f"{name}: {ver or 'desconocida'}")
