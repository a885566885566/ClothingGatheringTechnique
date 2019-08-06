from flask import Flask , render_template , request
app = Flask(__name__ , static_folder="./public")

'''
@app.route('/public')
def index(path):
    print("Get root")
    print(path)
    return send_from_directory(app.static_folder, path)
'''

@app.route('/public/<user>',methods=['GET'])
def index_name(user):
    return render_template('index.html' , user_template = user)

if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0" , port = 11230)
