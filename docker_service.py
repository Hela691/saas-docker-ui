import docker
from pathlib import Path
from docker.errors import NotFound
import shutil
def list_containers():
   
    client = docker.from_env()
    result = []

    for c in client.containers.list(all=True):
        # recharge pour être sûr d'avoir les ports à jour
        c.reload()

        ports = c.attrs.get("NetworkSettings", {}).get("Ports", {}) or {}

        # Simplifier l'affichage des ports
        exposed = []
        for container_port, bindings in ports.items():
            if not bindings:
                continue
            for b in bindings:
                exposed.append(f"{b.get('HostIp','0.0.0.0')}:{b.get('HostPort')} -> {container_port}")

        result.append({
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "image": (c.image.tags[0] if c.image.tags else "unknown"),
            "ports": exposed
        })

    return result

def start_container(container_id_or_name: str):
    client = docker.from_env()
    c = client.containers.get(container_id_or_name)
    c.start()

def stop_container(container_id_or_name: str):
    client = docker.from_env()
    c = client.containers.get(container_id_or_name)
    c.stop()

def delete_container(container_id_or_name: str):
    client = docker.from_env()
    c = client.containers.get(container_id_or_name)
    c.remove(force=True)
    name =c.name  
    site_dir = Path("user_sites") / name
    if site_dir.exists():
        shutil.rmtree(site_dir)

def get_used_ports():
    client = docker.from_env()
    used_ports = set()

    for c in client.containers.list(all=True):
        c.reload()
        ports = c.attrs.get("NetworkSettings", {}).get("Ports", {}) or {}
        for _, bindings in ports.items():
            if not bindings:
                continue
            for b in bindings:
                if b.get("HostPort"):
                    used_ports.add(int(b["HostPort"]))

    return used_ports

def find_free_port(start=8080, end=9000):
    used_ports = get_used_ports()

    for port in range(start, end + 1):
        if port not in used_ports:
            return port

    raise RuntimeError("Aucun port libre disponible")


def create_container(site_name: str, html_content: str):
    client = docker.from_env()

    # Nettoyer le nom (Docker-safe)
    slug = site_name.lower().replace(" ", "-")
    container_name = f"nginx_{slug}"

    # Trouver un port libre
    host_port = find_free_port()

    # Créer le dossier du site
    site_dir = Path("user_sites") / container_name
    site_dir.mkdir(parents=True, exist_ok=True)

    # Chemin absolu du fichier HTML
    html_path = (site_dir / "index.html").resolve()

    # Générer HTML si vide
    if not html_content:
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>{site_name}</title></head>
<body>
  <h1>{site_name}</h1>
  <p>Créé depuis Flask + Docker SDK</p>
</body>
</html>
"""

    # Écrire le fichier
    html_path.write_text(html_content, encoding="utf-8")

    # Supprimer l'ancien conteneur s'il existe
    try:
        old = client.containers.get(container_name)
        old.remove(force=True)
    except NotFound:
        pass

    # Créer et démarrer le conteneur Nginx
    client.containers.run(
        image="nginx:alpine",
        name=container_name,
        detach=True,
        ports={"80/tcp": host_port},
        volumes={
            str(html_path): {
                "bind": "/usr/share/nginx/html/index.html",
                "mode": "ro"
            }
        }
    )

    return container_name, host_port