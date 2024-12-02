from flask import Flask, make_response, jsonify, request
from bd import Alunos


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Vizualiza os alunos da lista
@app.route('/alunos', methods=['GET'])
def get_alunos():
    return make_response(
        jsonify(Alunos)
    )


# Adicionar  o aluno a lista
@app.route ('/alunos', methods= ['POST'])
def create_alunos():
    aluno = request.json 

    if not aluno.get("nome") or not aluno.get("semestre") or not aluno.get("notas") or len(aluno["notas"]) != 3:
        return jsonify({"error": "Dados inválidos. Certifique-se de que nome, semestre e 3 notas estão presentes."}), 400

    new_id = max([a["id"] for a in Alunos], default=0) + 1
    aluno["id"] = new_id  

    Alunos.append(aluno)

    return jsonify(aluno), 201

# Deleta o aluno da lista
@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    global Alunos  
    Alunos = [s for s in Alunos if s['id'] != id_aluno]  
    return jsonify({"message": "Aluno excluído com sucesso"}), 200

# Atualiza as informações do aluno na lista

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    aluno = next((s for s in Alunos if s['id'] == id_aluno), None)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    data = request.get_json()
    aluno.update({
        "nome": data.get("nome", aluno["nome"]),
        "semestre": data.get("semestre", aluno["semestre"]),
        "notas": data.get("notas", aluno["notas"]),
          })
    return jsonify(aluno), 200

if __name__ == '__main__':
    app.run(debug=True)