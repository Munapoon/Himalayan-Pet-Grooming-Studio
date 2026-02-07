import shutil
import os

source = r'C:\Users\Dell\.gemini\antigravity\brain\f59d98ad-5e36-4e17-a591-f84c371f819a\uploaded_media_1770200817541.png'
dest = r'C:\Users\Dell\Desktop\Himalayan Pet Grooming Studio\backend\media\hero_grooming.png'

if os.path.exists(source):
    shutil.copy(source, dest)
    print(f'✓ File copied successfully to {dest}')
    print(f'✓ File size: {os.path.getsize(dest)} bytes')
else:
    print(f'✗ Source file not found: {source}')
