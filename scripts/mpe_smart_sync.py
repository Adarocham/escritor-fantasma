import os
import subprocess
import datetime
import sys

def run_command(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output if hasattr(e, 'output') else e.stderr}"

def main():
    print("🧠 Iniciando Sincronización Inteligente MPE...")
    
    # 1. Verificar si estamos en un repositorio Git
    if not os.path.exists(".git"):
        print("❌ Error: No estás dentro de una carpeta de proyecto (Git).")
        return

    # 2. Verificar cambios
    status = run_command(["git", "status", "--short"])
    
    # 3. Pull preventivo (para evitar conflictos)
    print("📥 Trayendo cambios de la nube...")
    pull = run_command(["git", "pull", "origin", "main", "--rebase"])
    if "Error" in pull:
        print(f"⚠️  Aviso en el Pull: {pull}")

    if not status and "up to date" in pull.lower():
        print("✅ Todo está actualizado. Nada que sincronizar.")
        return

    # 4. Sincronizar cambios locales
    if status:
        print("📦 Cambios detectados. Preparando envío...")
        run_command(["git", "add", "."])
        
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        summary = sys.argv[1] if len(sys.argv) > 1 else "Sincronización automática"
        commit_msg = f"MPE Sync [{ts}]: {summary}"
        
        run_command(["git", "commit", "-m", commit_msg])
        print(f"📝 Commit realizado: {summary}")

    # 5. Push final
    print("📤 Subiendo todo a GitHub...")
    push = run_command(["git", "push", "origin", "main"])
    if "Error" in push:
        print(f"❌ Error al subir: {push}")
    else:
        print("✨ ¡Sincronización completada con éxito!")

if __name__ == "__main__":
    main()
