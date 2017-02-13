import json
import os
import re

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

SOLUTIONS_DIR = "solutions"


@app.route("/")
def home():
    solution_list = get_solution_list(SOLUTIONS_DIR)
    return render_template("index.html", solution_list=solution_list)


@app.route("/solution/<id>")
def solution(id):
    solution = retrieve_solution(SOLUTIONS_DIR, id)
    return render_template("solution.html", solution=solution)


@app.route("/compose", methods=["GET", "POST"])
def compose():
    if request.method == "POST":
        solution_id = store_solution(SOLUTIONS_DIR, request.form)
        return redirect("/solution/{}".format(solution_id))
    else:
        return render_template("compose.html")


def get_next_solution_id(directory):
    """
    Returns a suitable id for a new solution based on the contents of the specified directory.

    Parameters
    ----------
    directory : str

    Returns
    -------
    int

    """
    contents = os.listdir(directory)
    if len(contents) == 0:
        return 0
    id_list = [int(id_from_filename(filename)) for filename in contents]
    return max(id_list) + 1


def store_solution(directory, solution_dict):
    """
    Stores the new solution as a JSON file in the specified directory and returns its id.

    Parameters
    ----------
    directory : str
    solution_dict : dict

    Returns
    -------
    int

    """
    solution_id = get_next_solution_id(directory)
    path = os.path.join(directory, filename_from_id(solution_id))
    with open(path, "w") as fp:
        json.dump(solution_dict, fp)
    return solution_id


def retrieve_solution(directory, solution_id):
    """
    Retrieves the solution with the specified id from file.

    Parameters
    ----------
    directory : str
    solution_id : int

    Returns
    -------
    dict

    """
    path = os.path.join(directory, filename_from_id(solution_id))
    with open(path) as fp:
        return json.load(fp)


def filename_from_id(solution_id):
    """
    Returns a filename string for the solution id.

    Parameters
    ----------
    solution_id : int

    Returns
    -------
    str

    """
    return "solution_{}.json".format(solution_id)


def id_from_filename(filename):
    """
    Returns the solution id from a filename string.

    Parameters
    ----------
    filename : str

    Returns
    -------
    int

    """
    pattern = re.compile("solution_([0-9]+).json")
    match = pattern.match(filename)
    if match:
        return int(match.group(1))


def get_solution_list(directory):
    """
    Returns a list of summaries for solutions stored in the specified directory.

    Parameters
    ----------
    directory : str

    Returns
    -------
    list

    """
    contents = os.listdir(directory)
    solution_list = list()
    for filename in contents:
        solution_id = id_from_filename(filename)
        solution_dict = retrieve_solution(directory, solution_id)
        solution_list.append(dict(solution_id=solution_id,
                                  book=solution_dict["book"],
                                  author=solution_dict["author"],
                                  problem=solution_dict["problem"]))
    return solution_list


if __name__ == "__main__":
    app.run(debug=True)
