const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://jqsvainolbnhdtcvzzrn.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxc3ZhaW5vbGJuaGR0Y3Z6enJuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2ODI0NDEsImV4cCI6MjA5OTI1ODQ0MX0.nG_LBcl2qGVPubYMvFabheeuYkxiBMATw7tcSEJYICg';
const supabase = createClient(supabaseUrl, supabaseKey);

async function migrate() {
    try {
        console.log("Reading menu.js...");
        let menuJsContent = fs.readFileSync('menu.js', 'utf8');
        menuJsContent = menuJsContent.replace('const menuData = ', 'module.exports = ');
        fs.writeFileSync('menu_temp.js', menuJsContent);
        const menuData = require('./menu_temp.js');
        
        console.log(`Found ${menuData.length} categories.`);
        
        let sql = '';
        
        for (let i = 0; i < menuData.length; i++) {
            const cat = menuData[i];
            const catId = require('crypto').randomUUID();
            sql += `INSERT INTO categories (id, name, sort_order) VALUES ('${catId}', '${cat.category.replace(/'/g, "''")}', ${i});\n`;
            
            if (cat.items && cat.items.length > 0) {
                for (const item of cat.items) {
                    const selfPrice = item.self_price || 0;
                    const acPrice = item.ac_price || 0;
                    const imgUrl = item.image ? `'${item.image.replace(/'/g, "''")}'` : 'NULL';
                    sql += `INSERT INTO menu_items (category_id, name, self_price, ac_price, image_url) VALUES ('${catId}', '${item.name.replace(/'/g, "''")}', ${selfPrice}, ${acPrice}, ${imgUrl});\n`;
                }
            }
            sql += '\n';
        }
        
        fs.writeFileSync('insert_data.sql', sql);
        console.log("Generated insert_data.sql successfully!");
    } catch (e) {
        console.error("Migration failed:", e);
    }
}

migrate();
