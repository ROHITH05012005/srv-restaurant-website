-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create menu_items table
CREATE TABLE IF NOT EXISTS menu_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  self_price INTEGER NOT NULL,
  ac_price INTEGER NOT NULL,
  image_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;

-- Create site_config table for static images
CREATE TABLE IF NOT EXISTS site_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE site_config ENABLE ROW LEVEL SECURITY;

-- Create policies for categories (Public can read, authenticated users can write)
DROP POLICY IF EXISTS "Categories are viewable by everyone" ON categories;
CREATE POLICY "Categories are viewable by everyone" ON categories
  FOR SELECT USING (true);
  
DROP POLICY IF EXISTS "Categories are insertable by authenticated users" ON categories;
CREATE POLICY "Categories are insertable by authenticated users" ON categories
  FOR INSERT TO authenticated WITH CHECK (true);
  
DROP POLICY IF EXISTS "Categories are updatable by authenticated users" ON categories;
CREATE POLICY "Categories are updatable by authenticated users" ON categories
  FOR UPDATE TO authenticated USING (true);
  
DROP POLICY IF EXISTS "Categories are deletable by authenticated users" ON categories;
CREATE POLICY "Categories are deletable by authenticated users" ON categories
  FOR DELETE TO authenticated USING (true);

-- Create policies for menu_items
DROP POLICY IF EXISTS "Menu items are viewable by everyone" ON menu_items;
CREATE POLICY "Menu items are viewable by everyone" ON menu_items
  FOR SELECT USING (true);
  
DROP POLICY IF EXISTS "Menu items are insertable by authenticated users" ON menu_items;
CREATE POLICY "Menu items are insertable by authenticated users" ON menu_items
  FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "Menu items are updatable by authenticated users" ON menu_items;
CREATE POLICY "Menu items are updatable by authenticated users" ON menu_items
  FOR UPDATE TO authenticated USING (true);

-- Create policies for site_config
DROP POLICY IF EXISTS "Site config is viewable by everyone" ON site_config;
CREATE POLICY "Site config is viewable by everyone" ON site_config
  FOR SELECT USING (true);

DROP POLICY IF EXISTS "Site config is insertable by authenticated users" ON site_config;
CREATE POLICY "Site config is insertable by authenticated users" ON site_config
  FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "Site config is updatable by authenticated users" ON site_config;
CREATE POLICY "Site config is updatable by authenticated users" ON site_config
  FOR UPDATE TO authenticated USING (true);
  
DROP POLICY IF EXISTS "Menu items are deletable by authenticated users" ON menu_items;
CREATE POLICY "Menu items are deletable by authenticated users" ON menu_items
  FOR DELETE TO authenticated USING (true);

-- Create storage bucket for images
INSERT INTO storage.buckets (id, name, public) VALUES ('menu-images', 'menu-images', true) ON CONFLICT (id) DO NOTHING;

-- Enable RLS on storage
DROP POLICY IF EXISTS "Menu images are viewable by everyone" ON storage.objects;
CREATE POLICY "Menu images are viewable by everyone" 
ON storage.objects FOR SELECT USING (bucket_id = 'menu-images');

DROP POLICY IF EXISTS "Menu images are insertable by authenticated users" ON storage.objects;
CREATE POLICY "Menu images are insertable by authenticated users" 
ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id = 'menu-images');

DROP POLICY IF EXISTS "Menu images are updatable by authenticated users" ON storage.objects;
CREATE POLICY "Menu images are updatable by authenticated users" 
ON storage.objects FOR UPDATE TO authenticated USING (bucket_id = 'menu-images');

DROP POLICY IF EXISTS "Menu images are deletable by authenticated users" ON storage.objects;
CREATE POLICY "Menu images are deletable by authenticated users" 
ON storage.objects FOR DELETE TO authenticated USING (bucket_id = 'menu-images');
