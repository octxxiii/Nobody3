"""Convert st2.icns to icon.ico for Windows builds."""

import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, Qt

def convert_icns_to_ico():
    """Convert st2.icns to icon.ico."""
    icns_path = "st2.icns"
    ico_path = "icon.ico"
    
    if not os.path.exists(icns_path):
        print(f"Error: {icns_path} not found")
        return False
    
    # Load icon from icns file
    icon = QIcon(icns_path)
    
    if icon.isNull():
        print(f"Error: Failed to load icon from {icns_path}")
        return False
    
    # Create a pixmap with common Windows icon sizes
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    try:
        from PIL import Image
        
        import tempfile
        
        for size in sizes:
            pixmap = icon.pixmap(QSize(size, size))
            if not pixmap.isNull():
                # Save to temporary PNG file, then load with PIL
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    tmp_path = tmp.name
                
                if pixmap.save(tmp_path, 'PNG'):
                    # Load with PIL
                    img = Image.open(tmp_path)
                    # Convert to RGBA if needed
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    images.append(img)
                    # Clean up temp file
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
        
        if not images:
            print("Error: No valid icon sizes found")
            return False
        
        # Save as ICO with multiple sizes
        # PIL's ICO format: save the first image and it will include all sizes
        # when sizes parameter is provided correctly
        ico_sizes = [(img.width, img.height) for img in images]
        
        # Try saving with explicit sizes parameter
        # The ICO format should automatically include all provided sizes
        images[0].save(
            ico_path, 
            format='ICO',
            sizes=ico_sizes
        )
        
        # Verify the file was created and has reasonable size
        file_size = os.path.getsize(ico_path)
        print(f"Successfully created {ico_path} with {len(images)} sizes: {ico_sizes} (size: {file_size} bytes)")
        
        # If file is too small, it might not have included all sizes
        if file_size < 1000 and len(images) > 1:
            print(f"Warning: ICO file seems small ({file_size} bytes) for {len(images)} sizes")
            print("Trying alternative method: saving largest size only...")
            # Fallback: save the largest size
            largest_img = max(images, key=lambda x: x.width)
            largest_img.save(ico_path, format='ICO')
            file_size = os.path.getsize(ico_path)
            print(f"Saved largest size only ({largest_img.width}x{largest_img.height}): {file_size} bytes")
        
        return True
        
    except ImportError:
        print("Error: PIL/Pillow is required for ICO conversion")
        print("Install it with: pip install Pillow")
        return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

if __name__ == "__main__":
    # QApplication is required for QIcon/QPixmap
    app = QApplication(sys.argv)
    success = convert_icns_to_ico()
    sys.exit(0 if success else 1)

