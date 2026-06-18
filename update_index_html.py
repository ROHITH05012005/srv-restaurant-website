import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the hardcoded menu with dynamic containers
# Find from <div class="menu-tabs" id="menuTabs"> up to </section>\n  <!-- CHEF SPECIALS -->
pattern1 = re.compile(r'<div class="menu-tabs" id="menuTabs">.*?(?=</section>\s*<!-- CHEF SPECIALS -->)', re.DOTALL)

dynamic_html = """<div class="menu-tabs-scroll" id="menuTabs" style="display:flex; overflow-x:auto; white-space:nowrap; gap:1rem; padding-bottom:1rem; margin-bottom:2rem; scrollbar-width:thin; scrollbar-color:var(--gold) var(--black-soft);">
      <!-- Tabs generated dynamically -->
    </div>

    <div class="menu-grid" id="menuItemsGrid">
      <!-- Items generated dynamically -->
    </div>
"""

content = pattern1.sub(lambda m: dynamic_html, content)

# 2. Add <script src="menu.js"></script> just before the main <script> tag
if 'src="menu.js"' not in content:
    content = content.replace('<script>', '<script src="menu.js"></script>\n  <script>')

# 3. Replace switchTab and switchServiceType with dynamic logic
js_pattern = re.compile(r'let currentServiceType = \'ac\';.*?function switchTab\(tab\) {.*?(?=\n\s*// CART LOGIC)', re.DOTALL)

dynamic_js = """let currentServiceType = 'ac';
    let currentCategory = '';

    function switchServiceType(type) {
      currentServiceType = type;
      const btnAc = document.getElementById('btn-ac');
      const btnSelf = document.getElementById('btn-self');
      
      if(type === 'ac') {
        btnAc.style.background = 'linear-gradient(135deg,var(--gold),var(--saffron))';
        btnAc.style.color = 'var(--black)';
        btnAc.style.borderColor = 'var(--gold)';
        
        btnSelf.style.background = 'rgba(255,255,255,0.03)';
        btnSelf.style.color = 'var(--gold)';
        btnSelf.style.borderColor = 'rgba(212,175,55,0.3)';
      } else {
        btnSelf.style.background = 'linear-gradient(135deg,var(--gold),var(--saffron))';
        btnSelf.style.color = 'var(--black)';
        btnSelf.style.borderColor = 'var(--gold)';
        
        btnAc.style.background = 'rgba(255,255,255,0.03)';
        btnAc.style.color = 'var(--gold)';
        btnAc.style.borderColor = 'rgba(212,175,55,0.3)';
      }
      
      // Re-render items if a category is selected
      if (currentCategory) {
        renderItems(currentCategory);
      }
    }

    // Generate Menu Tabs
    function generateMenuTabs() {
      const tabsContainer = document.getElementById('menuTabs');
      tabsContainer.innerHTML = '';
      menuData.forEach((catData, index) => {
        const btn = document.createElement('button');
        btn.className = 'menu-tab' + (index === 0 ? ' active' : '');
        btn.innerText = catData.category;
        btn.onclick = () => switchTab(catData.category);
        tabsContainer.appendChild(btn);
      });
      if(menuData.length > 0) {
        switchTab(menuData[0].category);
      }
    }

    // MENU TABS
    function switchTab(category) {
      currentCategory = category;
      // Update active class on tabs
      document.querySelectorAll('.menu-tab').forEach(t => {
        if(t.innerText === category) t.classList.add('active');
        else t.classList.remove('active');
      });
      renderItems(category);
    }

    function renderItems(category) {
      const grid = document.getElementById('menuItemsGrid');
      grid.innerHTML = '';
      const catData = menuData.find(c => c.category === category);
      if(!catData) return;

      catData.items.forEach(item => {
        const price = currentServiceType === 'ac' ? item.ac_price : item.self_price;
        const idName = item.name.replace(/\\s+/g, '-');
        const card = document.createElement('div');
        card.className = 'food-card reveal';
        // Handle images
        let imgSrc = item.image;
        if (imgSrc === 'placeholder.png') {
          // generate a reliable placeholder or default
          imgSrc = 'logo.png';
        }
        card.innerHTML = `
            <div class="food-img-wrap">
              <img src="${imgSrc}" alt="${item.name}" class="food-img" loading="lazy">
              <div class="diet-tag veg"></div>
            </div>
            <div class="food-info">
              <div class="food-name">${item.name}</div>
              <div class="food-price">₹${price}</div>
              <div class="food-actions">
                <button class="add-btn" onclick="addToCart('${item.name}', ${price})">Add</button>
                <div class="qty-controls" id="qty-${idName}">
                  <button class="qty-btn" onclick="updateQty('${item.name}', -1, ${price})">-</button>
                  <span class="qty-val" id="val-${idName}">0</span>
                  <button class="qty-btn" onclick="updateQty('${item.name}', 1, ${price})">+</button>
                </div>
              </div>
            </div>
        `;
        grid.appendChild(card);
      });
      
      // Update UI for existing cart items
      updateCartUI();
    }
    
    // Initialize menu on load
    document.addEventListener('DOMContentLoaded', () => {
      if(typeof menuData !== 'undefined') {
        generateMenuTabs();
      }
    });
"""

content = js_pattern.sub(lambda m: dynamic_js, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")
