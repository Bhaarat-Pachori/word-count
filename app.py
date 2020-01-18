from flask import Flask, render_template, request, flash
from werkzeug import secure_filename
import frequent as fq

app = Flask(__name__)
app.secret_key = "random-secret-key"
app.config['DEBUG'] = True



@app.route('/')
def main_page():
    """
    this method is just the entry point to the
    main starting page.
    :return: upload.html page
    """
    return render_template('upload.html')


@app.route('/document', methods = ['GET', 'POST'])
def upload_file():
    """
    this method handles the file uploading and save it to the
    directory of where the code is run
    :return: renders the upload page again to the user
    """

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('upload.html')

        uploaded_file = request.files['file']
        if uploaded_file.filename == "":
            flash("No file selected for uploading")
            return render_template('upload.html')
        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            if uploaded_file.filename.split(".")[1] == "txt":
                uploaded_file.save(secure_filename(uploaded_file.filename))
                flash('File successfully uploaded')
                freq = fq.get_frequency(uploaded_file.filename)
                if type(freq) == str:
                    flash('File is empty')
                    return render_template('upload.html')
                else:
                    return render_template('frequencies.html', freq=freq)
        else:
            flash("Only text files are supported")
            return render_template('upload.html')


if __name__ == '__main__':
    app.run()