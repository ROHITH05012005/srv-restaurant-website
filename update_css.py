import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .food-card
html = re.sub(
    r'\.food-card\s*\{[^}]+\}',
    """.food-card {
      background: rgba(20, 20, 20, 0.7);
      border: 1px solid rgba(212, 175, 55, 0.1);
      border-radius: 16px;
      overflow: hidden;
      transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
      position: relative;
      cursor: pointer;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }""",
    html
)

html = re.sub(
    r'\.food-card:hover\s*\{[^}]+\}',
    """.food-card:hover {
      transform: translateY(-8px) scale(1.02);
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7), 0 0 20px rgba(212, 175, 55, 0.2);
      border-color: rgba(212, 175, 55, 0.5);
    }
    
    .food-card::before {
      content: '';
      position: absolute;
      top: 0; left: -100%;
      width: 50%; height: 100%;
      background: linear-gradient(to right, transparent, rgba(212, 175, 55, 0.08), transparent);
      transform: skewX(-25deg);
      transition: left 0.7s ease;
      z-index: 1;
      pointer-events: none;
    }
    .food-card:hover::before {
      left: 200%;
    }""",
    html
)

html = re.sub(
    r'\.food-card-img img\s*\{[^}]+\}',
    """.food-card-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.7s cubic-bezier(0.165, 0.84, 0.44, 1);
    }""",
    html
)

html = re.sub(
    r'\.food-card:hover \.food-card-img img\s*\{[^}]+\}',
    """.food-card:hover .food-card-img img {
      transform: scale(1.1) rotate(2deg);
    }""",
    html
)

# 2. Update .gallery-item
html = re.sub(
    r'\.gallery-item\s*\{[^}]+\}',
    """.gallery-item {
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      aspect-ratio: 1;
      cursor: pointer;
      transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }""",
    html
)

html = re.sub(
    r'\.gallery-item:hover\s*\{[^}]+\}',
    """.gallery-item:hover {
      transform: scale(1.04);
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
      z-index: 2;
    }""",
    html
)

# 3. Update buttons
html = re.sub(
    r'\.btn-primary\s*\{[^}]+\}',
    """.btn-primary {
      padding: 1.2rem 3rem;
      border: 1px solid var(--gold);
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(212, 175, 55, 0.05) 100%);
      backdrop-filter: blur(8px);
      color: var(--gold);
      font-family: 'Raleway', sans-serif;
      font-size: 1.1rem;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
      border-radius: 6px;
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
    }""",
    html
)

html = re.sub(
    r'\.btn-primary:hover\s*\{[^}]+\}',
    """.btn-primary:hover {
      background: var(--gold);
      color: var(--black);
      box-shadow: 0 0 35px rgba(212, 175, 55, 0.5);
      transform: translateY(-4px) scale(1.02);
    }""",
    html
)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated!")
