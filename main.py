from flask import Flask, render_template, request
import pyshorteners

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def url_short():
    short_url=None
    if request.method == 'POST':
        url=request.form['url']
        s=pyshorteners.Shortener()
        short_url=s.tinyurl.short(url)
    return render_template('index.html',short=short_url)
    

if __name__=="__main__":
    app.run(debug=True)