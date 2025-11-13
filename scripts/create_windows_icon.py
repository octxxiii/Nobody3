#!/usr/bin/env python3
"""
Windows용 ICO 아이콘 파일 생성 스크립트
"""

import os
import sys

def create_icon_ico():
    """Windows용 ICO 파일 생성"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 아이콘 크기들 (Windows ICO 파일에 포함될 크기)
        sizes = [16, 32, 48, 64, 128, 256]
        icon_images = []
        
        for size in sizes:
            # 새 이미지 생성 (투명 배경)
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 원형 배경 (다크 테마)
            margin = size // 8
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill=(45, 45, 45, 255), outline=(85, 85, 85, 255), width=max(1, size//32))
            
            # 텍스트 추가
            try:
                font_size = size // 3
                # Windows에서 사용 가능한 폰트 시도
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
        
        # ICO 파일 생성 (여러 크기 포함)
        if icon_images:
            # ICO 파일에는 보통 작은 크기만 포함 (16, 32, 48, 64)
            ico_sizes = [img for img in icon_images if img.size[0] in [16, 32, 48, 64]]
            if ico_sizes:
                ico_sizes[0].save('icon.ico', format='ICO', sizes=[(img.size[0], img.size[1]) for img in ico_sizes])
                print("✓ Windows 아이콘 생성됨: icon.ico")
            else:
                icon_images[0].save('icon.ico', format='ICO', sizes=[(img.size[0], img.size[1]) for img in icon_images[:4]])
                print("✓ Windows 아이콘 생성됨: icon.ico")
        else:
            print("❌ 아이콘 이미지를 생성할 수 없습니다.")
            
    except ImportError:
        print("❌ PIL(Pillow) 패키지가 필요합니다:")
        print("   pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ 아이콘 생성 중 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if create_icon_ico():
        print("✓ icon.ico 파일이 생성되었습니다.")
        sys.exit(0)
    else:
        print("⚠ 아이콘 생성에 실패했습니다. 수동으로 icon.ico 파일을 생성하거나 제공하세요.")
        sys.exit(1)

