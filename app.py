from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code = None
    if request.method == 'POST':
        url = request.form['url']
        color = request.form['color'][1:]  # Remove the '#' from the color hex code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill=f'rgb({int(color[0:2], 16)}, {int(color[2:4], 16)}, {int(color[4:6], 16)})', back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        qr_code = f"data:image/png;base64,{img_str}"

    return render_template('index.html', qr_code=qr_code)

if __name__ == '__main__':
    app.run(debug=True)
