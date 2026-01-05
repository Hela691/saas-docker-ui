from flask import Flask, render_template, redirect, url_for, request
from docker_service import list_containers, start_container, stop_container, delete_container , create_container

app = Flask(__name__)

# =========================
# PAGE PRINCIPALE
# =========================
@app.route("/")
def index():
    containers = list_containers()
    return render_template("index.html", containers=containers)


# =========================
# ACTIONS SUR CONTENEURS
# =========================
@app.route("/container/<cid>/start", methods=["POST"])
def container_start(cid):
    start_container(cid)
    return redirect(url_for("index"))


@app.route("/container/<cid>/stop", methods=["POST"])
def container_stop(cid):
    stop_container(cid)
    return redirect(url_for("index"))


@app.route("/container/<cid>/delete", methods=["POST"])
def container_delete(cid):
    delete_container(cid)
    return redirect(url_for("index"))


# =========================
# CREATE CONTAINER
# =========================
@app.route("/create", methods=["POST"])
def create():
    site_name = request.form.get("site_name", "").strip()
    html_content = request.form.get("html_content", "").strip()

    if not site_name:
        site_name = "mon-site"

    create_container(site_name, html_content)
    return redirect(url_for("index"))


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
