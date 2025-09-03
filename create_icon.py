#!/usr/bin/env python3
"""
간단한 아이콘 생성 스크립트
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        # 아이콘 크기들
        sizes = [16, 32, 48, 64, 128, 256]
        
        for size in sizes:
            # 새 이미지 생성 (투명 배경)
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 원형 배경
            margin = size // 8
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(45, 45, 45, 255), outline=(85, 85, 85, 255), width=2)
            
            # 텍스트 추가
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
            
            # PNG로 저장
            img.save(f'icon_{size}.png')
            print(f"아이콘 생성됨: icon_{size}.png")
        
        # ICO 파일 생성 (Windows용)
        try:
            icon_images = []
            for size in [16, 32, 48, 64]:
                icon_images.append(Image.open(f'icon_{size}.png'))
            
            icon_images[0].save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
            print("Windows 아이콘 생성됨: icon.ico")
        except Exception as e:
            print(f"ICO 생성 실패: {e}")
        
        # ICNS 파일 생성 (macOS용) - 외부 도구 필요
        print("macOS ICNS 파일을 생성하려면 다음 명령을 사용하세요:")
        print("iconutil -c icns icon.iconset")
        
        # iconset 폴더 생성
        iconset_dir = "icon.iconset"
        if not os.path.exists(iconset_dir):
            os.makedirs(iconset_dir)
        
        # macOS 아이콘 크기별 복사
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
        
        print(f"iconset 폴더 생성됨: {iconset_dir}")
        
    if __name__ == "__main__":
        create_icon()
        
except ImportError:
    print("PIL(Pillow) 패키지가 필요합니다:")
    print("pip install Pillow")