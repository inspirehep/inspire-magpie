import logging

from inspire_magpie import application

# Enable logging for wsgi server
if not application.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    application.logger.addHandler(stream_handler)
    wsgi_logger = logging.getLogger('wsgi.errors')
    wsgi_logger.addHandler(stream_handler)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5051, debug=True)
