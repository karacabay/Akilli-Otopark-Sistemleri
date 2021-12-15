from AkilliOtopark import app, db
from Create import create

if __name__ == '__main__':
    create()
    app.run(debug=False, host='0.0.0.0')

