import pathlib
css = pathlib.Path("site/assets/styles.css")
ext = pathlib.Path("_extra.css")
with open(css, "a", encoding="utf-8") as f:
    f.write(ext.read_text(encoding="utf-8"))
print(f"Appended {ext.stat().st_size} bytes")
