from supabase import create_client, Client

# 🔗 Configuração do Supabase
SUPABASE_URL = "https://oyxnleqakgfzsmnpwrnn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95eG5sZXFha2dmenNtbnB3cm5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MjA4NjYsImV4cCI6MjA1NjQ5Njg2Nn0.wSc9G3KKd75VlBdFjKgKdxeaLtnWs68YbH3LglAuLxE"

# 🔥 Criando a conexão com o Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
