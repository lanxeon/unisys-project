from unisys import app, socketio

if __name__=='__main__':
	#app.run(debug=True)
	#Going to run using socketio from here on
	socketio.run(app, debug=True)