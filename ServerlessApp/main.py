from Code import create_app, config

app = create_app()

if __name__ == '__main__':
    app.run(config.HOST, config.PORT, debug=config.DEBUG)
