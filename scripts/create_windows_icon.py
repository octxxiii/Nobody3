#!/usr/bin/env python3
"""
Windows??ICO ?„ì´ì½??Œì¼ ?ì„± ?¤í¬ë¦½íŠ¸
"""

import os
import sys

def create_icon_ico():
    """Windows??ICO ?Œì¼ ?ì„±"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # ?„ì´ì½??¬ê¸°??(Windows ICO ?Œì¼???¬í•¨???¬ê¸°)
        sizes = [16, 32, 48, 64, 128, 256]
        icon_images = []
        
        for size in sizes:
            # ???´ë?ì§€ ?ì„± (?¬ëª… ë°°ê²½)
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # ?í˜• ë°°ê²½ (?¤í¬ ?Œë§ˆ)
            margin = size // 8
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(45, 45, 45, 255), outline=(85, 85, 85, 255), width=max(1, size//32))
            
            # ?ìŠ¤??ì¶”ê?
            try:
                font_size = size // 3
                # Windows?ì„œ ?¬ìš© ê°€?¥í•œ ?°íŠ¸ ?œë„
                font_paths = [
                    "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/calibri.ttf",
                    "C:/Windows/Fonts/msyh.ttc",
                ]
                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        try:
                            font = ImageFont.truetype(font_path, font_size)
                            break
                        except:
                            continue
                
                if font is None:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            text = "Oct"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 - size // 16
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
            
            icon_images.append(img)
        
        # ICO ?Œì¼ ?ì„± (?¬ëŸ¬ ?¬ê¸° ?¬í•¨)
        if icon_images:
            # ICO ?Œì¼?ëŠ” ë³´í†µ ?‘ì? ?¬ê¸°ë§??¬í•¨ (16, 32, 48, 64)
            ico_sizes = [img for img in icon_images if img.size[0] in [16, 32, 48, 64]]
            if ico_sizes:
                ico_sizes[0].save('icon.ico', format='ICO', sizes=[(img.size[0], img.size[1]) for img in ico_sizes])
                print("??Windows ?„ì´ì½??ì„±?? icon.ico")
            else:
                icon_images[0].save('icon.ico', format='ICO', sizes=[(img.size[0], img.size[1]) for img in icon_images[:4]])
                print("??Windows ?„ì´ì½??ì„±?? icon.ico")
        else:
            print("???„ì´ì½??´ë?ì§€ë¥??ì„±?????†ìŠµ?ˆë‹¤.")
            
    except ImportError:
        print("??PIL(Pillow) ?¨í‚¤ì§€ê°€ ?„ìš”?©ë‹ˆ??")
        print("   pip install Pillow")
        return False
    except Exception as e:
        print(f"???„ì´ì½??ì„± ì¤??¤ë¥˜ ë°œìƒ: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if create_icon_ico():
        print("??icon.ico ?Œì¼???ì„±?˜ì—ˆ?µë‹ˆ??")
        sys.exit(0)
    else:
        print("???„ì´ì½??ì„±???¤íŒ¨?ˆìŠµ?ˆë‹¤. ?˜ë™?¼ë¡œ icon.ico ?Œì¼???ì„±?˜ê±°???œê³µ?˜ì„¸??")
        sys.exit(1)

