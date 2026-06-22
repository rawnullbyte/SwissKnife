from __future__ import annotations
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import PlainTextResponse
import qrcode
from PIL import Image

router = APIRouter()

@router.get("/qr")
async def qr(request: Request, data: str = None):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing 'data' query parameter"
        )
    
    # Code taken from https://github.com/nikelau/python-ascii-qr-generator/blob/main/python-ascii-qr-generator.py
    # Credits to nikelau

    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    
    qr.add_data(data)
    qr.make(fit=True)

    size = 1
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size * img.size[0], size * img.size[1]))
    
    ascii_qr = ""
    for y in range(0, img.size[1], 2):
        for x in range(img.size[0]):
            upper_pixel = img.getpixel((x, y))
            lower_pixel = img.getpixel((x, y+1)) if y+1 < img.size[1] else 255
            
            if upper_pixel == 0 and lower_pixel == 0:
                ascii_qr += "█"
            elif upper_pixel == 0 and lower_pixel == 255:
                ascii_qr += "▀"
            elif upper_pixel == 255 and lower_pixel == 0:
                ascii_qr += "▄"
            else:
                ascii_qr += " "
        ascii_qr += "\n"
    
    return PlainTextResponse(content=ascii_qr)