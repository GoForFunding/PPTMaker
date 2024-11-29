from flask import Flask, request, jsonify, send_file
from TextGen import GenText2
from pptMake import GenPPT
from PPTPicker import PickPPT
import os 

# Initialize Flask app
app = Flask(__name__)

@app.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    data = request.json  # Get the input data from POST request
    user_input = data.get('user_input', '')
    style=data.get('Style', '')
    #PPT Picker(style) and get the PPT
    file,slideInfo=PickPPT(style)
    '''file="modern4.pptx"
    slideInfo={"lenth":56,"p":1,"s":2,"m":4,"b":3}'''
    ppt=file
    outputFile=os.path.join(os.getcwd(), "temp.pptx")
    if not user_input:
        return jsonify({"error": "No user input provided."}), 400
    details=GenText2(user_input,slideInfo["length"],25)
    
    genrated=GenPPT(ppt,outputFile,details,slideInfo)
    if genrated:
        return send_file(outputFile, as_attachment=True, download_name="updated_pitch_deck.pptx")
    else:
        return False
if __name__ == '__main__':
    # Run the app
    app.run(debug=True, port=5000)