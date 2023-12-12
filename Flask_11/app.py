from flask import Flask, render_template
import json

'''utils'''


def load_candidates_from_json(path):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
        return {i['pk']: i for i in data}


data = load_candidates_from_json('..\candidates.json')


def get_candidate(pk):
    if pk in data:
        return data[pk]


def get_candidates_by_name(name):
    return [i for i in data.values() if name.lower() in i['name'].lower()]


def get_candidates_by_skill(skill):
    return [i for i in data.values() if skill.lower() in i['skills'].lower().split(', ')]


# ==============================================================================================

'''app'''

app = Flask(__name__)


@app.route('/')
def list():
    return render_template('list.html', candidates=data.values())


@app.route('/candidate/<int:pk>')
def candidate(pk):
    return render_template('single.html', candidate=get_candidate(pk))


@app.route('/search/<name>')
def search(name):
    candidates = get_candidates_by_name(name)
    return render_template('search.html', candidates=candidates, candidates_len=len(candidates))


@app.route('/skills/<skill>')
def skills(skill):
    skills = get_candidates_by_skill(skill)
    return render_template('skill.html', skills=skills, skills_len=len(skills), skill=skill)


app.run(debug=False)
