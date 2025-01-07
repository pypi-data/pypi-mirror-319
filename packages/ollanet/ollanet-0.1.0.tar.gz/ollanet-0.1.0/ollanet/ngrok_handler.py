from pyngrok import ngrok, conf, exception

def run_ngrok(protocol, port, authtoken):
    try:
        conf.get_default().auth_token = authtoken
        public_url = ngrok.connect(port, "http").public_url
        if protocol == "http":
            public_url = public_url.replace("https://", "http://")
        print(f"\nngrok tunnel created successfully!")
        print(f"Public URL: {public_url}")
        ngrok.get_ngrok_process().proc.wait()
    except exception.PyngrokError as e:
        print(f"Error: {e}")