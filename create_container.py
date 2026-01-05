import docker
from pathlib import Path
from docker.errors import NotFound

def main():
    client = docker.from_env()

    container_name = "nginx_python2"
    host_port = 8086
    html_path = Path("user_sites/nginx_python/index.html").resolve()

    # 1) supprimer l'ancien conteneur s'il existe
    try:
        old = client.containers.get(container_name)
        old.remove(force=True)
        print(f"🧹 Ancien conteneur supprimé: {container_name}")
    except NotFound:
        pass

    # 2) créer le nouveau
    client.containers.run(
        image="nginx:alpine",
        name=container_name,
        detach=True,
        ports={"80/tcp": host_port},
        volumes={
            str(html_path): {
                "bind": "/usr/share/nginx/html/index.html",
                "mode": "ro",
            }
        },
    )

    print(f"✅ Conteneur créé: {container_name} sur http://<IP_VM>:{host_port}")

if __name__ == "__main__":
    main()


