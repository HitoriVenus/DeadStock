from deadstock import create_app
import deadstock.config as config

if __name__ == "__main__":
    app = create_app(__name__)
    app.run(
        host=config.cfg.program.host,
        port=config.cfg.program.port,
        debug=config.cfg.program.debug
    )