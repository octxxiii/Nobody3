#!/usr/bin/env python3
"""
Í∞ÑÎã®???ÑÏù¥ÏΩ??ùÏÑ± ?§ÌÅ¨Î¶ΩÌä∏
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        # ?ÑÏù¥ÏΩ??¨Í∏∞??
        sizes = [16, 32, 48, 64, 128, 256]
        
        for size in sizes:
            # ???¥Î?ÏßÄ ?ùÏÑ± (?¨Î™Ö Î∞∞Í≤Ω)
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # ?êÌòï Î∞∞Í≤Ω
            margin = size // 8
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(45, 45, 45, 255), outline=(85, 85, 85, 255), width=2)
            
            # ?çÏä§??Ï∂îÍ?
            try:
                font_size = size // 4
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text = "Oct"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
            
            # PNGÎ°??Ä??
            img.save(f'icon_{size}.png')
            print(f"?ÑÏù¥ÏΩ??ùÏÑ±?? icon_{size}.png")
        
        # ICO ?åÏùº ?ùÏÑ± (Windows??
        try:
            icon_images = []
            for size in [16, 32, 48, 64]:
                icon_images.append(Image.open(f'icon_{size}.png'))
            
            icon_images[0].save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
            print("Windows ?ÑÏù¥ÏΩ??ùÏÑ±?? icon.ico")
        except Exception as e:
            print(f"ICO ?ùÏÑ± ?§Ìå®: {e}")
        
        # ICNS ?åÏùº ?ùÏÑ± (macOS?? - ?∏Î? ?ÑÍµ¨ ?ÑÏöî
        print("macOS ICNS ?åÏùº???ùÏÑ±?òÎ†§Î©??§Ïùå Î™ÖÎ†π???¨Ïö©?òÏÑ∏??")
        print("iconutil -c icns icon.iconset")
        
        # iconset ?¥Îçî ?ùÏÑ±
        iconset_dir = "icon.iconset"
        if not os.path.exists(iconset_dir):
            os.makedirs(iconset_dir)
        
        # macOS ?ÑÏù¥ÏΩ??¨Í∏∞Î≥?Î≥µÏÇ¨
        mac_sizes = {
            16: "icon_16x16.png",
            32: "icon_16x16@2x.png",
            32: "icon_32x32.png", 
            64: "icon_32x32@2x.png",
            128: "icon_128x128.png",
            256: "icon_128x128@2x.png",
            256: "icon_256x256.png",
        }
        
        for size, filename in mac_sizes.items():
            if os.path.exists(f'icon_{size}.png'):
                import shutil
                shutil.copy(f'icon_{size}.png', os.path.join(iconset_dir, filename))
        
        print(f"iconset ?¥Îçî ?ùÏÑ±?? {iconset_dir}")
        
    if __name__ == "__main__":
        create_icon()
        
except ImportError:
    print("PIL(Pillow) ?®ÌÇ§ÏßÄÍ∞Ä ?ÑÏöî?©Îãà??")
    print("pip install Pillow")
