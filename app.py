from praatio import textgrid
from robyn import Response, Robyn

FN = "Adamie_aanniajuartitaq"

app = Robyn(__file__)
app.serve_directory("/static", directory_path="static")

tg = textgrid.openTextgrid(f"aligned/{FN}.TextGrid", includeEmptyIntervals=False)
phones = [(e.start, e.end, e.label) for e in tg.getTier("phones").entries]


@app.get("/audio")
async def audio(request):
    with open(f"to_align/{FN}.wav", "rb") as f:
        data = f.read()
    return Response(
        status_code=200, headers={"Content-Type": "audio/wav"}, description=data
    )


@app.get("/")
async def index(request):
    spans = " ".join(
        f'<span data-start="{s}" data-end="{e}">{l}</span>' for s, e, l in phones
    )
    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
      <div id="phonemes">{spans}</div>
      <audio id="audio" controls src="/audio"></audio>
      <script>
        const audio = document.getElementById("audio");
        const spans = document.querySelectorAll("#phonemes span");
        function update() {{
          const t = audio.currentTime;
          spans.forEach(s => s.classList.toggle("active", t >= +s.dataset.start && t < +s.dataset.end));
          requestAnimationFrame(update);
        }}
        requestAnimationFrame(update);
      </script>
    </body>
    </html>"""
    return Response(
        status_code=200, headers={"Content-Type": "text/html"}, description=html
    )


app.start(host="0.0.0.0", port=8080)
