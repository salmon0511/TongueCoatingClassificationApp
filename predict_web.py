import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from keras.models import Sequential, load_model
import keras, sys
import numpy as np
from PIL import Image
import keras.backend as K
import tensorflow as tf

# Blueprint宣言
# from flask import Blueprint
#
# js = Blueprint("javascript", __name__, static_url_path='/js', static_folder='./static/js')
# css = Blueprint("css", __name__, static_url_path='/css', static_folder='./static/css')
# image = Blueprint("image", __name__, static_url_path='/image', static_folder='./static/image')
class_1 = "1です。"
class_content_1 = "舌苔はほとんどついておらず、かなり綺麗な状態かと思われます。"
classes_solution_1 = "これまでと同様に、口腔ケアを頑張っていきましょう。注意点として、舌磨きのやりすぎは舌を傷つけるだけでなく舌苔の付着量増加にもつながるため、１日１回を限度に優しく行うようにしましょう。"

class_2 = "2です。"
class_content_2 = "舌の汚れはあまり気にする必要はないでしょう。"
classes_solution_2 = "舌苔は口臭の原因にもなるため、ああああああああああああああああああああああああああああああああああああああああああああああああああああ。"

class_3 = "3です。"
class_content_3 = "舌に汚れが若干多くついているかもしれません。舌苔（舌の汚れ）は口臭の原因にもなるため、普段の歯磨きに加え、舌を掃除することが望ましいでしょう。"
classes_solution_3 = "舌苔の掃除法としてはガーゼや舌ブラシを用いて、舌の表面を奥から手前に優しくこするようにして行ってください。1日1回を限度に行いましょう。"

classes = [class_1,class_2,class_3]
classes_content = [class_content_1, class_content_2, class_content_3]
classes_solution = [classes_solution_1, classes_solution_2, classes_solution_3]

num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIOS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model('./tongue_cnn_aug.h5')
graph = tf.get_default_graph()



def allowed_file(filename):
    #もし.が含まれたる　かつ　もし拡張子前の.で区切り、拡張子小文字小文字であれば　true
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIOS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('ファイルがありません')
                return redirect(request.url)
            file = request.files['file']
            # if user does not selectfile, browser also
            #submit an empty part without filename
            if file.filename == '':
                flash('ファイルがありません')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                image = Image.open(filepath)
                image = image.convert('RGB')
                image = image.resize((image_size, image_size))
                data = np.asarray(image)
                X = []
                X.append(data)
                X = np.array(X)

                #model = load_model('./tongue_cnn_aug.h5')

                result = model.predict([X])[0]
                predicted = result.argmax()
                percentage = int(result[predicted] * 100)
                #K.clear_session()
                result_title = ""
                result_content=""
                result_solution=""

                return render_template('test.html', result = classes[predicted], result_content = classes_content[predicted], result_solution = classes_solution[predicted], result_title="解析結果")


                #return redirect(url_for('upload_file', filename=filename))

        return render_template('test.html')





from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

