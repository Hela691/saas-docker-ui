import docker

def main():
    client = docker.from_env()

    print("✅ Connexion Docker OK")
    containers = client.containers.list(all=True)

    print(f"📦 Nombre de conteneurs trouvés: {len(containers)}")
    for c in containers:
        print(f"- name={c.name} status={c.status} id={c.short_id}")

if __name__ == "__main__":
    main()
