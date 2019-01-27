from buzzwebpanel import app, db, flash_errors, config_setting
from models import GameServer, Match
import util

from flask import Blueprint, request, render_template, flash, g, redirect

from wtforms import Form, validators, StringField, IntegerField, BooleanField


server_blueprint = Blueprint('server', __name__)


class ServerForm(Form):
    display_name = StringField('Display Name',
                               validators=[
                                   validators.Length(min=-1,
                                                     max=GameServer.display_name.type.length)])

    ip_string = StringField('Server IP',
                            validators=[
                                validators.required(),
                                validators.IPAddress()])

    port = IntegerField('Server port', default=27015,
                        validators=[validators.required()])

    rcon_password = StringField('RCON password',
                                validators=[
                                    validators.required(),
                                    validators.Length(min=-1,
                                                      max=GameServer.rcon_password.type.length)])

    public_server = BooleanField('Publicly usable server')


@server_blueprint.route('/server/create', methods=['GET', 'POST'])
def server_create():

    form = ServerForm(request.form)
    if request.method == 'POST':
        num_servers = GameServer.query.count()
        max_servers = config_setting('USER_MAX_SERVERS')
        if max_servers >= 0 and num_servers >= max_servers:
            flash('You already have the maximum number of servers ({}) stored'.format(
                num_servers))

        elif form.validate():
            mock = config_setting('TESTING')

            data = form.data
            server = GameServer.create(data['display_name'],
                                       data['ip_string'], data['port'],
                                       data['rcon_password'],
                                       True)

            if mock or util.check_server_connection(server):
                db.session.commit()
                app.logger.info(
                    'Created server {}'.format(server.id))
                return redirect('/servers')
            else:
                db.session.remove()
                flash('Failed to connect to server')

        else:
            flash_errors(form)

    return render_template('server_create.html', form=form,
                           edit=False, is_admin=True)


@server_blueprint.route('/server/<int:serverid>/edit', methods=['GET', 'POST'])
def server_edit(serverid):
    server = GameServer.query.get_or_404(serverid)

    form = ServerForm(request.form,
                      display_name=server.display_name,
                      ip_string=server.ip_string,
                      port=server.port,
                      rcon_password=server.rcon_password,
                      public_server=server.public_server)

    if request.method == 'POST':
        if form.validate():
            mock = app.config['TESTING']

            data = form.data
            server.display_name = data['display_name']
            server.ip_string = data['ip_string']
            server.port = data['port']
            server.rcon_password = data['rcon_password']
            server.public_server = True

            if mock or util.check_server_connection(server):
                db.session.commit()
                return redirect('/servers')
            else:
                db.session.remove()
                flash('Failed to connect to server')

        else:
            flash_errors(form)

    return render_template('server_create.html', form=form,
                           edit=True, is_admin=True)


@server_blueprint.route('/server/<int:serverid>/delete', methods=['GET'])
def server_delete(serverid):
    server = GameServer.query.get_or_404(serverid)
    is_owner = True
    if not is_owner:
        return 'Not your server', 400

    if server.in_use:
        return 'Cannot delete when in use', 400

    matches = Match.query.filter_by(server_id=serverid)
    for m in matches:
        m.server_id = None

    GameServer.query.filter_by(id=serverid).delete()
    db.session.commit()
    return redirect('myservers')


@server_blueprint.route("/servers")
def servers():
    servers = GameServer.query.order_by(-GameServer.id).limit(50)

    return render_template('servers.html', servers=servers)
