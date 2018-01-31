import service
import configuration

configuration.init_db(service.app)

# instead of threaded there should be some web server before flask app
service.app.run(threaded=True, host='0.0.0.0')

