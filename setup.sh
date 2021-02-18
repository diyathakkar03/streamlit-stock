mkdir -p ~/.streamlit/
echo "[general]
email = \"thakkar.b@northeastern.edu\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml