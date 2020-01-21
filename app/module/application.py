from flask import render_template, request
from app import app
from app.module.sweet import Sweet
from matplotlib import pyplot as plt
import os
import scipy.cluster.hierarchy as sch


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global sweet
    file = request.files["file"]
    n_cluster = int(request.form["cluster"])

    # Save file to tmp/
    file.save(os.path.join('app/tmp', 'dataset.xlsx'))

    # Load dataset with Sweet library
    sweet = Sweet(file="app/tmp/dataset.xlsx", cluster=n_cluster)
    return render_template("view_data.html", tables=[sweet.get_data().to_html(classes='table table-bordered')])


@app.route("/process", methods=["GET"])
def process():
    global sweet
    # Transform dataset
    X = sweet.transform()

    # Clusterizing process
    sch.dendrogram(sch.linkage(X, method='ward'))
    plt.savefig("static/images/dendrogram.png")

    # Modelling cluster
    sweet.get_cluster()

    # Get plot for visualization data
    sweet.plot()
    return render_template("result.html", dendrogram="dendrogram.png", plot="plot.png")
