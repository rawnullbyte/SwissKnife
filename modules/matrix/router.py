from __future__ import annotations
import asyncio
import random
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, PlainTextResponse

router = APIRouter()

WIDTH  = 80
HEIGHT = 24
FPS    = 20
FRAME_TIME = 1.0 / FPS

GLYPHS = (
    "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
    "0123456789ABCDEFZ"
)

DIM    = 22
MID    = 34
BRIGHT = 46
HEAD   = 231
DECAY  = [22, 22, 28, 34, 40, 46]

def esc(fg: int, bold: bool = False) -> str:
    b = "\033[1m" if bold else "\033[22m"
    return f"\033[38;5;{fg}m{b}"

RESET = "\033[0m\033[22m"


class Column:
    def __init__(self, x: int):
        self.x = x
        self.reset()

    def reset(self):
        self.head   = random.randint(-HEIGHT, 0)
        self.length = random.randint(6, HEIGHT - 2)
        self.speed  = random.choice([1, 1, 1, 2])   # rows per frame
        self.chars  = [random.choice(GLYPHS) for _ in range(HEIGHT)]
        self.glitch_timer = 0

    def tick(self):
        self.head += self.speed
        self.glitch_timer -= 1
        if self.glitch_timer <= 0:
            self.glitch_timer = random.randint(2, 8)
            row = random.randint(0, HEIGHT - 1)
            self.chars[row] = random.choice(GLYPHS)
        if self.head - self.length > HEIGHT:
            self.reset()

    def char_at(self, row: int) -> tuple[str, int] | None:
        dist = self.head - row
        if dist < 0 or dist >= self.length:
            return None
        if dist == 0:
            return self.chars[row], HEAD
        tail_pos = min(dist - 1, len(DECAY) - 1)
        color = DECAY[-(tail_pos + 1)]
        return self.chars[row], color


async def matrix_generator():
    cols = [Column(x) for x in range(WIDTH)]

    hide_cursor  = "\033[?25l"
    show_cursor  = "\033[?25h"
    clear_screen = "\033[2J\033[H"
    home         = "\033[H"

    try:
        yield hide_cursor + clear_screen

        while True:
            for col in cols:
                col.tick()

            lines = []
            for row in range(HEIGHT):
                row_parts = []
                for col in cols:
                    result = col.char_at(row)
                    if result is None:
                        row_parts.append(f"\033[38;5;{DIM}m ")
                    else:
                        glyph, color = result
                        bold = (color == HEAD)
                        row_parts.append(f"{esc(color, bold)}{glyph}")
                lines.append("".join(row_parts) + RESET)

            frame = home + "\n".join(lines)
            yield frame
            await asyncio.sleep(FRAME_TIME)

    except GeneratorExit:
        yield show_cursor


@router.get("/matrix")
async def matrix(request: Request):
    ua = request.headers.get("user-agent", "").lower()
    if "curl" not in ua:
        return PlainTextResponse(
            "Please curl this endpoint :D\n\n",
            status_code=418,
        )
    return StreamingResponse(
        matrix_generator(),
        media_type="text/plain",
    )