from gettext import translation
from bottle import *
from jinja2 import Environment, FileSystemLoader
from web.controllers.languageController import LanguageController
from web.controllers.mailController import MailController
from web.controllers.navigationController import NavigationController
from web.controllers.cameraController import CameraController
from web.controllers.projectController import ProjectController
from web.i18n.PoParser import PoParser


class LibreScanWeb:

    def __init__(self):
        self.host = 'localhost'
        self.port = '8181'
        self.app = Bottle()
        self.default_language = 'spa'
        self.env = self.init_environment()
        self.controllers = self.init_controllers()
        self.init_routes()

    def init_environment(self):
        env = Environment(loader=FileSystemLoader(searchpath='views/'),
                            extensions=['pyjade.ext.jinja.PyJadeExtension', 'jinja2.ext.i18n'])
        translations = translation(domain='messages', localedir='./i18n/locale', languages=[self.default_language])
        env.install_gettext_translations(translations)
        return env

    def init_routes(self):
        self._init_language_routes()
        self._init_mail_routes()
        self.app.route('/assets/:p_file#.+#', name='static', callback=self.return_resource)
        self.app.route('/', method="GET", callback=self.controllers['navigation'].home)
        self.app.route('/language/<lang>', method="GET", callback=self.controllers['language'].change_language)
        self.app.route('/project/<id>/config', method="GET", callback=self.controllers['project'].get_config)
        self.app.route('/project', method="POST", callback=self.controllers['project'].create)
        self.app.route('/project/new', method="GET", callback=self.controllers['project'].new)

    def _init_language_routes(self):
        self.app.route('/photo', method="POST", callback=self.controllers['camera'].create)  # Route to handle shoot.
        self.app.route('/photo', method="PUT", callback=self.controllers['camera'].update)  # Route to handle recapture.
        self.app.route('/photo', method="DELETE", callback=self.controllers['camera'].delete)  # Route to handle delete.
        self.app.route('/photo', method="GET", callback=self.controllers['camera'].get)  # Route to handle get photo.

    def _init_mail_routes(self):
        self.app.route('/mail', method="POST", callback=self.controllers['mail'].create)


        # The other routes would go here.

    def init_controllers(self):
        controllers = {
            'navigation': NavigationController(self.env),
            'camera': CameraController(self.env),
            'project': ProjectController(self.env),
            'mail': MailController(self.env),
            'language': LanguageController(self.env)
        }

        return controllers

    def return_resource(self, p_file):
        print(p_file)
        return static_file(p_file, root='assets')

    def run_app(self):
        PoParser.compile_po_files()
        self.app.run(host=self.host, port=self.port, quiet=False, debug=True)


app = LibreScanWeb()
app.run_app()
