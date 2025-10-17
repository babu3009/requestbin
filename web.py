from requestbin import config
import os

from requestbin import app, socketio

if __name__ == "__main__":
    port = int(os.environ.get('PORT', config.PORT_NUMBER))
    socketio.run(app, host='0.0.0.0', port=port, debug=config.DEBUG)