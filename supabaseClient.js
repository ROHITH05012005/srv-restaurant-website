const SUPABASE_URL = 'https://jqsvainolbnhdtcvzzrn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxc3ZhaW5vbGJuaGR0Y3Z6enJuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM2ODI0NDEsImV4cCI6MjA5OTI1ODQ0MX0.nG_LBcl2qGVPubYMvFabheeuYkxiBMATw7tcSEJYICg';

// Initialize Supabase client globally with a safe name
window.supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
