from flask import Flask, render_template, url_for, request, redirect, send_file
from product import Product
from data_conversion import dict_list_to_file
from livereload import Server


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extraction')
def extract():
    return render_template('extraction.html')


@app.route('/get-opinions', methods=['GET', 'POST'])
def get_opinions():
    if request.method == "POST":
        product_code = request.form['product_code']
        if product_code:
            return redirect('/product/'+product_code)
        else:
            feedback = 'You haven\'t entered correct product code'
            return render_template('/extraction.html', feedback=feedback)

    return render_template('/extraction.html')


@app.route('/product/<product_code>')
def display_product(product_code):
    product = Product(product_code)
    return render_template('/product.html', product=product)


@app.route('/product/<product_code>/download-opinions/<file_type>')
def download_opinions(product_code, file_type):
    product = Product(product_code)
    file_name = f'{product_code}.{file_type}'
    file_path = f'./opinions/{product_code}'
    dict_list_to_file(product.opinions, file_path, file_name, file_type)
    try:
        return send_file(file_path+'/'+file_name, as_attachment=True, attachment_filename=file_name)
    except Exception as e:
        return str(e)


@app.route('/product/<product_code>/statistics')
def display_statistics(product_code):
    return render_template('/statistics.html')


if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
"""
# old version, just runs the app
if __name__ == "__main__":
    app.run()
"""
