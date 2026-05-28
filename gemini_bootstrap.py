import os
import sys
import subprocess
import site
import importlib

def setup_environment():
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "--break-system-packages", "google-genai"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        importlib.reload(site)
    except:
        pass

def run_genai(api_key, input_data):
    try:
        from google import genai
    except ImportError:
        print("[-] google-genai Library fehlt.")
        return
    
    client = genai.Client(api_key=api_key)
    
    # Diese Namen stammen direkt aus deiner Liste:
    models_to_try = [
        'models/gemini-2.0-flash',
        'models/gemini-pro-latest',
        'models/gemini-flash-latest',
        'models/gemini-2.5-flash'
    ]
    
    success = False
    for m_id in models_to_try:
        if success: break
        try:
            print(f"[*] Kontaktiere {m_id}...")
            res = client.models.generate_content(
                model=m_id, 
                contents=f"Hardware-Info:\n{input_data}",
                config={'system_instruction': "Du bist ein Gentoo-Hardened-Ingenieur. Antworte nur in Linux-Befehlen."}
            )
            print(f"\n=== KI-INSTALLATIONSPLAN ===\n{res.text}\n")
            success = True
        except Exception as e:
            err = str(e)
            if "429" in err:
                print(f"[-] {m_id}: Quota voll (Warte kurz...).")
            else:
                print(f"[-] {m_id} fehlgeschlagen: {err[:50]}...")
            continue
    
    if not success:
        print("[-] Alle Versuche gescheitert. Bitte 30 Sek. warten (Rate Limit).")

if __name__ == "__main__":
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("[-] GEMINI_API_KEY fehlt!"); sys.exit(1)
    if not sys.stdin.isatty():
        setup_environment()
        run_genai(key, sys.stdin.read())
