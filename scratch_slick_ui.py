import re

def update_css(content):
    # 1. Navbar Glassmorphism
    content = content.replace(
        """
    nav {
      position: fixed;
      top: 0;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem 5%;
      z-index: 100;
      transition: all 0.4s ease;
    }
""",
        """
    nav {
      position: fixed;
      top: 0;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem 5%;
      z-index: 100;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      border-bottom: 1px solid transparent;
    }
    nav.scrolled {
      padding: 1rem 5%;
      background: rgba(10, 10, 10, 0.7);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(212, 175, 55, 0.15);
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
"""
    )
    # Remove old nav.scrolled if present
    content = re.sub(r'nav\.scrolled\s*\{[^}]+\}', '', content, count=1)
    
    # 2. Hero buttons upgrade
    content = content.replace(
        """
    .hero-btn {
      padding: 1rem 2.5rem;
      border: 2px solid var(--gold);
      background: transparent;
      color: var(--gold);
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: color 0.4s;
    }
""",
        """
    .hero-btn {
      padding: 1rem 2.5rem;
      border: 1px solid var(--gold);
      background: rgba(212, 175, 55, 0.05);
      backdrop-filter: blur(4px);
      color: var(--gold);
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
      box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
      border-radius: 4px;
    }
    .hero-btn:hover {
      background: var(--gold);
      color: var(--black);
      box-shadow: 0 0 30px rgba(212, 175, 55, 0.4);
      transform: translateY(-3px);
    }
"""
    )

    # 3. Food Card Upgrades
    content = content.replace(
        """
    .food-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(212, 175, 55, 0.1);
      border-radius: 8px;
      overflow: hidden;
      transition: transform 0.3s, border-color 0.3s;
      position: relative;
    }

    .food-card:hover {
      transform: translateY(-10px);
      border-color: rgba(212, 175, 55, 0.4);
    }
""",
        """
    .food-card {
      background: rgba(20, 20, 20, 0.6);
      border: 1px solid rgba(212, 175, 55, 0.08);
      border-radius: 12px;
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      position: relative;
      backdrop-filter: blur(10px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .food-card:hover {
      transform: translateY(-8px) scale(1.02);
      border-color: rgba(212, 175, 55, 0.5);
      box-shadow: 0 15px 40px rgba(212, 175, 55, 0.15);
    }
    
    .food-card::before {
      content: '';
      position: absolute;
      top: 0; left: -100%;
      width: 50%; height: 100%;
      background: linear-gradient(to right, transparent, rgba(212, 175, 55, 0.05), transparent);
      transform: skewX(-25deg);
      transition: left 0.7s;
      z-index: 1;
    }
    
    .food-card:hover::before {
      left: 200%;
    }
"""
    )

    # 4. Gallery Grid Upgrades
    content = content.replace(
        """
    .gallery-item {
      position: relative;
      overflow: hidden;
      border-radius: 8px;
      aspect-ratio: 1;
      cursor: pointer;
    }
""",
        """
    .gallery-item {
      position: relative;
      overflow: hidden;
      border-radius: 12px;
      aspect-ratio: 1;
      cursor: pointer;
      transition: all 0.5s ease;
    }
    .gallery-item:hover {
      transform: scale(1.03);
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
      z-index: 2;
    }
"""
    )
    
    # 5. Food Image Hover effect
    content = content.replace(
        """
    .food-card-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s;
    }
    
    .food-card:hover .food-card-img img {
      transform: scale(1.1);
    }
""",
        """
    .food-card-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .food-card:hover .food-card-img img {
      transform: scale(1.15) rotate(2deg);
    }
"""
    )

    return content

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_html = update_css(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("CSS Upgrades applied!")
