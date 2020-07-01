from flask import *
import pickle

monthData = pickle.load( open( "monthData.pkl", "rb" ) )
dayData = pickle.load( open( "dayData.pkl", "rb" ) )
mostActiveAccounts = pickle.load( open( "mostActiveAccounts.pkl", "rb" ) )
mostFollowedAccounts = pickle.load( open( "mostFollowedAccounts.pkl", "rb" ) )
mostViralAccounts = pickle.load( open( "mostViralAccounts.pkl", "rb" ) )
negativeReasons = pickle.load( open( "neg_reasons.pickle", "rb" ) )
data={
	'monthData':monthData,
	'dayData': dayData,
	'mostActiveAccounts':mostActiveAccounts,
	'mostFollowedAccounts':mostFollowedAccounts,
	'mostViralAccounts':mostViralAccounts,
	'negativeReasons':negativeReasons
}

app= Flask(__name__)

@app.route('/india')
def india():
	return render_template('india.html')

@app.route('/indiaData')
def indiaData():
	print('get request')
	return data
@app.route('/world')
def world():
	return render_template('world.html')

if __name__ == '__main__':
	app.run(debug=True)
