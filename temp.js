
    // CURSOR
    const cursor = document.getElementById('cursor');
    const ring = document.getElementById('cursorRing');
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      cursor.style.left = mx - 5 + 'px'; cursor.style.top = my - 5 + 'px';
    });
    function animRing() {
      rx += (mx - rx) * .1; ry += (my - ry) * .1;
      ring.style.left = rx - 18 + 'px'; ring.style.top = ry - 18 + 'px';
      requestAnimationFrame(animRing);
    }
    animRing();
    document.querySelectorAll('a,button,.food-card,.gallery-item').forEach(el => {
      el.addEventListener('mouseenter', () => { ring.style.width = '50px'; ring.style.height = '50px'; ring.style.borderColor = 'var(--saffron)'; });
      el.addEventListener('mouseleave', () => { ring.style.width = '36px'; ring.style.height = '36px'; ring.style.borderColor = 'var(--gold)'; });
    });

    // NAV SCROLL
    window.addEventListener('scroll', () => {
      const nav = document.getElementById('navbar');
      if (window.scrollY > 60) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    });

    // MOBILE NAV
    function toggleNav() {
      document.getElementById('navLinks').classList.toggle('open');
    }
    document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open')));

    let currentServiceType = 'ac';
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
        btn.className = 'menu-tab';
        if (!currentCategory && index === 0) btn.classList.add('active');
        if (currentCategory === catData.category) btn.classList.add('active');
        btn.innerText = catData.category;
        btn.onclick = () => switchTab(catData.category);
        tabsContainer.appendChild(btn);
      });
      
      const addCatBtn = document.createElement('button');
      addCatBtn.className = 'add-category-btn';
      addCatBtn.innerText = '+ Add Category';
      addCatBtn.onclick = addNewCategory;
      tabsContainer.appendChild(addCatBtn);

      if(menuData.length > 0 && !currentCategory) {
        switchTab(menuData[0].category);
      } else if (currentCategory) {
        switchTab(currentCategory);
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
        const idName = item.name.replace(/\s+/g, '-');
        const card = document.createElement('div');
        card.className = 'food-card';
        // Handle images
        let imgSrc = item.image;
        if (imgSrc === 'placeholder.png' || !imgSrc) {
          imgSrc = 'logo.png';
        }
        card.innerHTML = `
            <div class="food-card-img">
              <img src="${imgSrc}" alt="${item.name}" loading="lazy">
              <div class="veg-badge"><div class="veg-dot"></div></div>
              <button class="edit-img-btn" onclick="editItemImage('${item.name.replace(/'/g, "\\'")}')">✏️</button>
            </div>
            <div class="food-card-body">
              <div class="food-name">${item.name}</div>
              <div class="food-price">
                ₹${price}
                <button class="edit-details-btn" onclick="editItemDetails('${item.name.replace(/'/g, "\\'")}')">✏️</button>
              </div>
              <div class="food-actions">
                <button class="add-btn" onclick="addToCart(this, '${item.name.replace(/'/g, "\\'")}', ${price})">Add</button>
                <div class="qty-controls" data-item="${item.name}">
                  <button class="qty-btn" onclick="updateQty('${item.name.replace(/'/g, "\\'")}', -1)">-</button>
                  <span class="qty-num">0</span>
                  <button class="qty-btn" onclick="updateQty('${item.name.replace(/'/g, "\\'")}', 1)">+</button>
                </div>
              </div>
            </div>
        `;
        grid.appendChild(card);
        if (typeof VanillaTilt !== 'undefined') {
          VanillaTilt.init(card, {
            max: 12, speed: 400, glare: true, "max-glare": 0.15, scale: 1.03
          });
        }
      });
      
      const addItemCard = document.createElement('div');
      addItemCard.className = 'food-card add-item-card';
      addItemCard.onclick = () => addNewItem(category);
      addItemCard.innerHTML = `<div style="font-size:2rem; color:var(--gold); margin-bottom:10px;">+</div><div style="color:var(--gold); font-weight:bold;">Add New Item</div>`;
      grid.appendChild(addItemCard);

      // Update UI for existing cart items
      updateCartUI();
    }
    


    // CART SYSTEM
    let cart = {};

    function toggleCart() {
      const drawer = document.getElementById('cartDrawer');
      drawer.classList.toggle('open');
    }

    function addToCart(btn, name) {
      // Get price from sibling span
      const priceText = btn.previousElementSibling.textContent;
      const price = parseInt(priceText.replace('₹', ''));

      if (!cart[name]) {
        cart[name] = { price: price, qty: 1 };

        // UI Update: Swap Add button for Qty controls
        btn.style.display = 'none';
        const controls = btn.nextElementSibling;
        controls.classList.add('active');
        controls.querySelector('.qty-num').textContent = 1;

        updateCartUI();
      }
    }

    function updateQty(name, delta) {
      if (cart[name]) {
        cart[name].qty += delta;

        if (cart[name].qty <= 0) {
          delete cart[name];

          // UI Reset: Swap back to Add button
          const controls = document.querySelector(`.qty-controls[data-item="${name}"]`);
          if (controls) {
            controls.classList.remove('active');
            controls.previousElementSibling.style.display = 'block';
          }
        } else {
          const controls = document.querySelector(`.qty-controls[data-item="${name}"]`);
          if (controls) controls.querySelector('.qty-num').textContent = cart[name].qty;
        }

        updateCartUI();
      }
    }

    function updateCartUI() {
      const list = document.getElementById('cartItemsList');
      const countEl = document.getElementById('cartCount');
      const totalEl = document.getElementById('cartTotal');
      const float = document.getElementById('cartFloat');

      let total = 0;
      let count = 0;
      let itemsHTML = '';

      for (const [name, data] of Object.entries(cart)) {
        total += data.price * data.qty;
        count += data.qty;
        itemsHTML += `
      <div class="cart-item-row">
        <div class="item-info">
          <span class="item-name">${name}</span>
          <span class="item-price-each">₹${data.price} × ${data.qty}</span>
        </div>
        <div class="qty-controls active" data-item="${name}">
          <button class="qty-btn" onclick="updateQty('${name}', -1)">−</button>
          <span class="qty-num">${data.qty}</span>
          <button class="qty-btn" onclick="updateQty('${name}', 1)">+</button>
        </div>
      </div>
    `;
      }

      if (count === 0) {
        list.innerHTML = '<div class="empty-cart-msg">Your cart is empty</div>';
      } else {
        list.innerHTML = itemsHTML;
        // Animation for cart float
        float.style.transform = 'translateY(-50%) scale(1.1)';
        setTimeout(() => float.style.transform = 'translateY(-50%) scale(1)', 200);
      }

      countEl.textContent = count;
      totalEl.textContent = `₹${total}`;
    }

    function placeOrder() {
      if (Object.keys(cart).length === 0) {
        alert("Please add some items to your cart first!");
        return;
      }

      // Official Zomato Restaurant Link
      const zomatoLink = "https://www.zomato.com/bangalore/sri-raghavendra-vaibhava-koramangala-3rd-block-bangalore/order";

    function renderSpecials() {
      if (typeof specialsData === 'undefined') return;
      const container = document.getElementById('specialsContainer');
      if (!container) return;
      
      let htmlStr = '';
      specialsData.forEach(sp => {
        htmlStr += `
          <div class="special-card">
            <div style="position:relative; height:250px;">
              <img src="${sp.image}" alt="${sp.name}" style="width:100%;height:100%;object-fit:cover;">
              <button class="admin-only-btn" onclick="editItemImage('${sp.name.replace(/'/g, "\\'")}')">✏️</button>
            </div>
            <div class="special-overlay">
              <div class="special-tag">${sp.tag}</div>
              <div class="special-name">${sp.name}</div>
              <div class="special-price">
                ₹${sp.price} • ${sp.desc} 
                <button class="edit-details-btn" onclick="editSpecialDetails('${sp.name.replace(/'/g, "\\'")}')" style="margin-left:10px;">✏️</button>
              </div>
            </div>
          </div>
        `;
      });
      container.innerHTML = htmlStr;
      
      if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(container.querySelectorAll('.special-card'), {
          max: 10, speed: 400, glare: true, "max-glare": 0.2, scale: 1.03
        });
      }
    }

    // LIGHTBOX
    function openLightbox(src) {
      document.getElementById('lightboxImg').src = src;
      document.getElementById('lightbox').classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
      document.getElementById('lightbox').classList.remove('open');
      document.body.style.overflow = '';
    }

    // SCROLL REVEAL
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); } });
    }, { threshold: .12 });
    document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

    // Initialize menu on load
    if (typeof menuData !== 'undefined') {
      generateMenuTabs();
    }
    if (typeof specialsData !== 'undefined') {
      renderSpecials();
    }

    // COUNTERS
    const counterObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const el = e.target;
          const target = parseInt(el.dataset.target);
          let count = 0;
          const step = Math.max(1, Math.floor(target / 60));
          const timer = setInterval(() => {
            count = Math.min(count + step, target);
            el.textContent = count;
            if (count >= target) clearInterval(timer);
          }, 25);
          counterObs.unobserve(el);
        }
      });
    }, { threshold: .5 });
    document.querySelectorAll('.counter').forEach(el => counterObs.observe(el));

    // PARTICLE CANVAS
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    const particles = [];
    for (let i = 0; i < 60; i++) {
      particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        r: Math.random() * 2 + .5,
        vx: (Math.random() - .5) * .3,
        vy: -Math.random() * .5 - .2,
        a: Math.random() * .6 + .1,
        color: Math.random() > .5 ? '212,175,55' : '255,107,0'
      });
    }
    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.color},${p.a})`;
        ctx.fill();
        p.x += p.vx; p.y += p.vy;
        if (p.y < -10) p.y = canvas.height + 10;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
      });
      requestAnimationFrame(drawParticles);
    }
    drawParticles();

    let currentEditItem = null;

    function getGithubToken() {
      let token = localStorage.getItem('gh_pat');
      if (!token) {
        alert("You must be logged in as Admin to perform this action.");
      }
      return token;
    }

    function openAdminModal(title, bodyText) {
      document.getElementById('adminModalTitle').innerText = title;
      document.getElementById('adminModalBody').innerText = bodyText;
      document.getElementById('adminModalSpinner').style.display = 'none';
      document.getElementById('adminModal').style.display = 'block';
    }

    function closeAdminModal() {
      document.getElementById('adminModal').style.display = 'none';
      currentEditItem = null;
    }

    async function saveMenuToGithub(message) {
      const token = getGithubToken();
      if (!token) return;

      openAdminModal("Saving Changes", "Updating menu.js on GitHub... Please wait.");
      document.getElementById('adminModalSpinner').style.display = 'block';

      try {
        let jsContent = "const menuData = " + JSON.stringify(menuData, null, 4) + ";\n";
        if (typeof specialsData !== 'undefined') {
          jsContent += "\nconst specialsData = " + JSON.stringify(specialsData, null, 4) + ";\n";
        }
        const jsBase64 = btoa(unescape(encodeURIComponent(jsContent)));
        await uploadFileToGithub('menu.js', jsBase64, message, token, true);
        
        document.getElementById('adminModalBody').innerText = "Success! The menu is saved. Netlify will update the live site shortly.";
        document.getElementById('adminModalSpinner').style.display = 'none';
        
        // Re-render
        generateMenuTabs();
        if (typeof renderSpecials === 'function') renderSpecials();
        
      } catch (err) {
        console.error(err);
        document.getElementById('adminModalBody').innerText = "Error: " + err.message;
        document.getElementById('adminModalSpinner').style.display = 'none';
        if (err.message.includes('401')) {
          localStorage.removeItem('gh_pat'); 
          document.getElementById('adminModalBody').innerText += "\nInvalid token. Please try again.";
        }
      }
    }

    function editStaticImage(imagePath) {
      currentEditItem = 'STATIC:' + imagePath;
      openAdminModal("Paste Image", "Press CTRL+V to paste your new image. It will replace the existing one exactly.");
    }

    function editSpecialDetails(specialName) {
      let foundSpecial = specialsData.find(s => s.name === specialName);
      if (!foundSpecial) return;

      const newName = prompt("Edit Special Name:", foundSpecial.name);
      if (newName === null) return; 

      const newPrice = prompt("Edit Price:", foundSpecial.price);
      if (newPrice === null) return; 

      const newDesc = prompt("Edit Description (e.g. Unlimited):", foundSpecial.desc);
      if (newDesc === null) return;

      const newTag = prompt("Edit Tag (e.g. ⭐ Chef's Pick):", foundSpecial.tag);
      if (newTag === null) return;

      foundSpecial.name = newName.trim();
      foundSpecial.price = parseInt(newPrice) || 0;
      foundSpecial.desc = newDesc.trim();
      foundSpecial.tag = newTag.trim();

      saveMenuToGithub(`Edit special details: ${foundSpecial.name}`);
    }

    function addNewCategory() {
      const catName = prompt("Enter new Category Name:");
      if (!catName || catName.trim() === "") return;
      
      if (menuData.find(c => c.category.toLowerCase() === catName.toLowerCase())) {
        alert("Category already exists!");
        return;
      }
      
      menuData.push({ category: catName.trim(), items: [] });
      saveMenuToGithub(`Add new category: ${catName.trim()}`);
    }

    function addNewItem(category) {
      const itemName = prompt(`Add new item to ${category}\n\nEnter Item Name:`);
      if (!itemName || itemName.trim() === "") return;
      
      const selfPrice = prompt("Enter Self-Service Price (Numbers only):", "0");
      if (selfPrice === null) return;
      
      const acPrice = prompt("Enter AC Price (Numbers only):", "0");
      if (acPrice === null) return;
      
      const catData = menuData.find(c => c.category === category);
      if (catData) {
        catData.items.push({
          name: itemName.trim(),
          self_price: parseInt(selfPrice) || 0,
          ac_price: parseInt(acPrice) || 0,
          image: "logo.png"
        });
        saveMenuToGithub(`Add new item: ${itemName.trim()} to ${category}`);
      }
    }

    function editItemDetails(itemName) {
      let foundItem = null;
      for (let cat of menuData) {
        let itm = cat.items.find(i => i.name === itemName);
        if (itm) { foundItem = itm; break; }
      }
      if (!foundItem) return;

      const newName = prompt("Edit Item Name:", foundItem.name);
      if (newName === null) return; 

      const newSelfPrice = prompt("Edit Self-Service Price:", foundItem.self_price);
      if (newSelfPrice === null) return; 

      const newAcPrice = prompt("Edit AC Price:", foundItem.ac_price);
      if (newAcPrice === null) return; 

      foundItem.name = newName.trim();
      foundItem.self_price = parseInt(newSelfPrice) || 0;
      foundItem.ac_price = parseInt(newAcPrice) || 0;

      saveMenuToGithub(`Edit item details: ${foundItem.name}`);
    }

    function editItemImage(itemName) {
      currentEditItem = itemName;
      openAdminModal("Paste Image", "Press CTRL+V to paste your image for " + itemName + ".");
    }

    window.addEventListener('paste', async e => {
      if (!currentEditItem) return;
      if (document.getElementById('adminModal').style.display === 'none') return;

      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      let blob = null;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf("image") === 0) {
          blob = items[i].getAsFile();
          break;
        }
      }
      if (!blob) {
        alert("No image found in clipboard. Please copy an image and try again.");
        return;
      }

      const token = getGithubToken();
      if (!token) return;

      document.getElementById('adminModalBody').innerText = "Uploading image to GitHub... Please wait.";
      document.getElementById('adminModalSpinner').style.display = 'block';

      try {
        const base64Data = await convertBlobToBase64(blob);
        const b64 = base64Data.split(',')[1]; 
        
        if (currentEditItem.startsWith('STATIC:')) {
          const staticPath = currentEditItem.split(':')[1];
          await uploadFileToGithub(staticPath, b64, `Update static image ${staticPath}`, token, true);
          document.getElementById('adminModalBody').innerText = "Success! Image updated. Netlify will publish it shortly.";
          document.getElementById('adminModalSpinner').style.display = 'none';
          return;
        }

        const safeName = currentEditItem.replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const extension = blob.type.split('/')[1] || 'png';
        const imagePath = `assets/images/${safeName}_${Date.now()}.${extension}`;

        await uploadFileToGithub(imagePath, b64, `Update image for ${currentEditItem}`, token);

        document.getElementById('adminModalBody').innerText = "Updating menu.js... Please wait.";

        let foundInMenu = false;
        for (let cat of menuData) {
          let item = cat.items.find(i => i.name === currentEditItem);
          if (item) {
            item.image = imagePath;
            foundInMenu = true;
            break;
          }
        }
        
        if (!foundInMenu && typeof specialsData !== 'undefined') {
          let sp = specialsData.find(s => s.name === currentEditItem);
          if (sp) {
            sp.image = imagePath;
            foundInMenu = true;
          }
        }

        if (foundInMenu) {
          let jsContent = "const menuData = " + JSON.stringify(menuData, null, 4) + ";\n";
          if (typeof specialsData !== 'undefined') {
            jsContent += "\nconst specialsData = " + JSON.stringify(specialsData, null, 4) + ";\n";
          }
          const jsBase64 = btoa(unescape(encodeURIComponent(jsContent)));
          await uploadFileToGithub('menu.js', jsBase64, `Update image for ${currentEditItem}`, token, true);
        }

        document.getElementById('adminModalBody').innerText = "Success! Image updated. Netlify will publish it shortly.";
        document.getElementById('adminModalSpinner').style.display = 'none';
        
        generateMenuTabs();
        if (typeof renderSpecials === 'function') renderSpecials();
        
      } catch (err) {
        console.error(err);
        document.getElementById('adminModalBody').innerText = "Error: " + err.message;
        document.getElementById('adminModalSpinner').style.display = 'none';
        if (err.message.includes('401')) {
          localStorage.removeItem('gh_pat'); 
          document.getElementById('adminModalBody').innerText += "\nInvalid token. Please try again.";
        }
      }
    });

    function convertBlobToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onerror = reject;
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(blob);
      });
    }

    async function uploadFileToGithub(path, base64Content, message, token, getSha = false) {
      const owner = "ROHITH05012005";
      const repo = "srv-restaurant-website";
      const url = `https://api.github.com/repos/${owner}/${repo}/contents/${path}`;
      
      let sha = null;
      if (getSha) {
        const res = await fetch(url, { headers: { "Authorization": `token ${token}` } });
        if (res.ok) {
          const data = await res.json();
          sha = data.sha;
        }
      }

      const body = { message: message, content: base64Content, branch: "main" };
      if (sha) body.sha = sha;

      const response = await fetch(url, {
        method: 'PUT',
        headers: { "Authorization": `token ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(`GitHub API Error: ${response.status} - ${errData.message}`);
      }
      return await response.json();
    }

    function initAdminMode() {
      if (localStorage.getItem('gh_pat')) {
        document.body.classList.add('admin-mode');
        const btn = document.getElementById('navAdminBtn');
        if (btn) {
          btn.innerText = "Admin Logout";
          btn.href = "#";
        }
      }
    }
    initAdminMode();

    function toggleAdminLogin(e) {
      if (localStorage.getItem('gh_pat')) {
        if (e) e.preventDefault();
        if (confirm("You are currently logged in as Admin. Do you want to logout?")) {
          localStorage.removeItem('gh_pat');
          document.body.classList.remove('admin-mode');
          const btn = document.getElementById('navAdminBtn');
          if (btn) {
            btn.innerText = "Admin Login";
            btn.href = "admin.html";
          }
        }
        return false;
      }
      return true;
    }
  