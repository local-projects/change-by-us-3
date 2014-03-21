# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2013 Local Projects, all rights reserved
    :license: Affero GNU GPL v3, see LICENSE for more details.
"""

import os

from flask import Blueprint, request, render_template, redirect, current_app, url_for, request, g
from flask.ext.login import login_required, current_user, login_user
from flask.ext.security.utils import encrypt_password
from flask.ext.cdn_rackspace import upload_rackspace_image
from flask.ext.wtf.html5 import URLField
from flask.ext.wtf import ( Form, TextField, TextAreaField, FileField, BooleanField, 
                            SubmitField, Required, ValidationError, 
                            PasswordField, HiddenField)

from .models import User
from .helpers import _create_user, _delete_user, _unflag_user

from changebyus.helpers.stringtools import bool_strings


from changebyus.helpers.flasktools import jsonify_response, ReturnStructure, as_multidict
from changebyus.helpers.mongotools import db_list_to_dict_list 

from changebyus.modules.twitter.twitter import _get_user_name_and_thumbnail
from changebyus.modules.facebook.facebook import _get_fb_user_name_and_thumbnail

user_api = Blueprint('user_api', __name__, url_prefix='/api/user')


"""
.. module: user/api

    Users and projects are the core components of CBU.  This user api lets
    other modules create/modify/edit user information through various routines.
"""

class CreateUserForm(Form):

    email = TextField("email", validators=[Required()])
    password = PasswordField("password", validators=[Required()])
    display_name = TextField("display_name", validators=[Required()])
    first_name = TextField("first_name", validators=[Required()])
    last_name = TextField("last_name", validators=[Required()])
    bio = TextField()
    website = URLField()
    location = HiddenField("location")
    lat = HiddenField("lat")
    lon = HiddenField("lon")


@user_api.route('/create', methods = ['POST'])
def api_create_user():
    """Method to create a user account

        Args:
            email: email for user account
            password: password for user account
            display_name: users display name
            first_name: users first name
            last_name: users last name
            bio: short bio of user
            website: user website
            location: location of user
            lat: lat of user location
            lon: lon of user location

        Returns:
            Logs in user and returns the user data structure

    """

    if not g.user.is_anonymous():
        errStr = "You can not create an account when logged in." 
        return jsonify_response( ReturnStructure(msg = errStr, success = False) )

    form = CreateUserForm(request.form or as_multidict(request.json))
    if not form.validate():
        errStr = "Request contained errors."
        return jsonify_response( ReturnStructure( success = False, 
                                                  msg = errStr ) )

    email = form.email.data
    password = form.password.data
    display_name = form.display_name.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    bio = form.bio.data
    website = form.website.data
    location = form.location.data
    lat = form.lat.data
    lon = form.lon.data
    
    if (lat and lon):
        geo_location = [float(lon), float(lat)]
    else:
        geo_location = None

    errStr = ''
    display_name_user = User.objects(display_name=display_name)
    if display_name_user.count() > 0:
        # TODO display name error
        errStr += "Sorry, user name/display name '{0}' is already in use. ".format(display_name)

    email_user = User.objects(email=email) 
    if email_user.count() > 0:
        # TODO display email error
        errStr += "Sorry, email address '{0}' is already in use.".format(email)

    if len(errStr) > 0:
        return jsonify_response( ReturnStructure(msg = errStr, success = False) )  

    u = _create_user(email=email,
                     password=password,
                     display_name=display_name,
                     first_name=first_name,
                     last_name=last_name,
                     bio=bio,
                     website=website,
                     location=location,
                     geo_location=geo_location)

    if u is None:
        errStr += "Sorry, user creation failed."
        return jsonify_response( ReturnStructure(msg = errStr, success = False) )

    login_user(u)

    # if the user signed up from a page of importance, such as a project page
    # then send them back to where they came from
    return jsonify_response( ReturnStructure( data = u.as_dict() ))


@user_api.route('/<user_id>')    
# @login_required # not sure if this is needed
def api_get_user(user_id):
    """Routine to retrieve a user record
  
        Returns:
            User record if user found
    """

    u = User.objects(id=user_id, active=True).first()
     
    if u is None:
        ret = ReturnStructure( msg = "User not found.",
                               success = False,
                               data = {} )

        return jsonify_response( ret )

    ret = ReturnStructure( data = u.as_dict() )

    # Remove email from visibility
    if g.user.is_anonymous() or current_user.id != u.id:
        if not u.public_email:
            if ret.data.has_key('email'):
                ret.data['email'] = None
        
    return jsonify_response( ret )


class BetterBooleanField(BooleanField):
    false_values = ('false', 'False', '', False)

class EditUserForm(Form):
    email = TextField("email")
    public_email = BooleanField("public_email")
    password = PasswordField("password")
    display_name = TextField("display_name")
    first_name = TextField("first_name")
    last_name = TextField("last_name")
    bio = TextField()
    website = TextField()
    location = HiddenField("location")
    lat = HiddenField("lat")
    lon = HiddenField("lon")
    

@user_api.route('/edit', methods = ['POST'])
@login_required
def api_edit_user():
    """Routine to edit a user record

        Args:
            email: email for user account
            public_email: bool to determine if email is public
            password: password for user account
            display_name: users display name
            first_name: users first name
            last_name: users last name
            bio: short bio of user
            website: user website
            location: location of user
            lat: lat of user location
            lon: lon of user location   
            photo: user image         

        Returns:
            New user record if successful

    """

    form = EditUserForm(request.form or as_multidict(request.json))
    if not form.validate():
        errStr = "Request contained errors."
        return jsonify_response( ReturnStructure( success = False, 
                                                  msg = errStr ) )

    u = User.objects.with_id(g.user.id)

    # we have to access a BooleanFields raw_data when we are not using HTML forms

    email = form.email.data
    public_email = form.public_email.data
    password = form.password.data
    display_name = form.display_name.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    bio = form.bio.data
    website = form.website.data
    location = form.location.data
    lat = form.lat.data
    lon = form.lon.data
    
    if email: u.email = email
    if password: u.password = password
    if display_name: u.display_name = display_name
    if first_name: u.first_name = first_name
    if last_name: u.last_name = last_name
    if bio: u.bio = bio
    if website: u.website = website
    if location: u.location = location

    u.public_email = public_email
    
    if (lat and lon):
        u.geo_location = [float(lon), float(lat)]

    file_name = None

    # photo is optional
    if 'photo' in request.files:
        photo = request.files.get('photo')

        if len(photo.filename) > 3:

            try:
                result = upload_rackspace_image( photo )

                if result.success:
                    file_name = result.name
                    file_path = result.path
                    image_url = result.url

                    from .models import user_images

                    for manipulator in user_images:

                        manip_image = manipulator.converter(file_path)
                        base, extension = os.path.splitext(file_name)
                        manip_image_name = manipulator.prefix + '.' + base + manipulator.extension

                        if not upload_rackspace_image( manip_image.image, 
                                                       manip_image_name).success:

                            return jsonify_response( ReturnStructure ( success = False ) )
                else:
                    return jsonify_response( ReturnStructure ( success = False ) )

            except Exception as e:
                current_app.logger.exception(e)
                msg = "An error occured."
                return jsonify_response( ReturnStructure( success = False, 
                                                          msg = msg ) )

            file_name = result.name

        else:
            # again, photo optional
            file_name = None

    # we don't store the URL because the URL can change depending on what
    # rackspace container we wish to use
    if file_name:
        u.image_name = file_name


    u.save()

    # defaults to success and 'OK'
    return jsonify_response( ReturnStructure( data = u.as_dict() ) )


@user_api.route('/<user_id>', methods = ['DELETE'])
@user_api.route('/remove', methods = ['POST'])
def api_delete_user(user_id=None):
    if (not user_id):
        form = request.form if request.form else as_multidict(request.json)
        user_id = form.get('user_id')
    
    _delete_user(user_id)
    
    return jsonify_response(ReturnStructure())


@user_api.route('/<user_id>/unflag', methods = ['POST'])
def api_unflag_user(user_id=None):    
    _unflag_user(user_id)
    
    return jsonify_response(ReturnStructure())


@user_api.route('/socialstatus', methods = ['GET'])
@login_required
def api_get_user_social_status():
    """Method to query the social connectivity of the currently logged in user

        Returns:
            A dict containing True/False entries for the different supported social networks
    """

    user = User.objects.with_id(g.user.id)
    data = { 'facebook' : True if user.facebook_id else False,
             'twitter' : True if user.twitter_id else False }

    return jsonify_response( ReturnStructure( data = data ) )    


@user_api.route('/socialinfo', methods = ['GET'])
def api_get_user_social_info():
    """Method to query a users social information such as twitter and facebook name

        Returns:
            Current users name/image for various social platforms (if connected to those platforms)
         
    """

    twitter_info = _get_user_name_and_thumbnail()
    facebook_info = _get_fb_user_name_and_thumbnail()
    twitter_name = twitter_info[1]
    twitter_image = twitter_info[2]
    fb_name = facebook_info[1]
    fb_image = facebook_info[2]

    data = { 'twitter_name' : twitter_name,
             'twitter_image' : twitter_image,
             'fb_name' : fb_name,
             'fb_image' : fb_image,
             'id': str(g.user.id),
             'display_name': str(g.user.display_name),
             'email': str(g.user.email)
           }

    return jsonify_response( ReturnStructure( data = data ) )
    
@user_api.route('/list')
def api_get_users():
    """Returns a simple list of users, optionally sorted and limited
   
        Args:
            limit: limit of number of users to return
            sort: sort parameter
            order: order by parameter

        Returns:
            list of users dictionaries

    """
    limit = int(request.args.get('limit', 100))
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')
    
    # using raw query here so that most list queries aren't needlessly 
    # using flags__gt=-1 or something
    query = {"active":True}
    if bool(request.args.get('flagged', False)):
        query['flags'] = {"$gt":0}

    if (sort):
        sort_order = "%s%s" % (("-" if order == 'desc' else ""), sort)
        users = User.objects(__raw__=query).order_by(sort_order)
    else:
        users = User.objects(__raw__=query)

    users = users[0:limit]
    users_list = db_list_to_dict_list(users)

    print "user query",query, users_list

    return jsonify_response( ReturnStructure( data = users_list ) )    


@user_api.route('/<user_id>/flag', methods = ['POST'])
@login_required
def api_flag_user(user_id):
    u = User.objects.with_id(user_id)
    
    u.flags += 1
    u.save()

    return jsonify_response(ReturnStructure())


# TODO what is this doing here?
# make sure things work with it commented out
'''
@user_api.route('/encrypt', methods = ['POST', 'GET'])
def api_encrypt():
    """
    A utility API call that encrypts a string using the same algorithm and 
    salt as the application.
    """
    if (request.method == 'POST'):
        s = request.form['string']
    else:
        s = request.args.get('string')
    
    return gen_ok(jsonify({'encrypted': encrypt_password(s)}))
'''

