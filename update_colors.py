import sys

file_path = r'c:\Users\Dell\Desktop\Himalayan Pet Grooming Studio\frontend\static\css\user_profile.css'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '#6366f1': '#1e3a8a',
    '#8b5cf6': '#1d4ed8',
    '#a855f7': '#3b82f6',
    'rgba(99, 102, 241': 'rgba(30, 58, 138',
    'rgba(139, 92, 246': 'rgba(29, 78, 216',
    '#4f46e5': '#172554',
    '#818cf8': '#3b82f6',
    '#475569, #64748b': '#1e3a8a, #1d4ed8'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Colors updated successfully.')
