TODO: DOCUMENTATION PENDING
===========================

- [ ] Add documentation in PSMDOC format
- [ ] Add examples of send email, PUSH NOTIFICATIONS, SMS, etc
- [ ] Add examples of create roles and permissions in multi project support
- [ ] Add examples of request_handler usage to validate permissions, ownership, etc

=========
NETS CORE
=========

And set of lazy API request handlers and common tasks. 
Just use it if you are really sure that you don't want to 
repeat common tasks in request from many sources.

REQUIREMENTS
____________
This package requires the following packages that will be installed automatically:

    Django
    pytz 
    python-dateutil
    shortuuid 
    django-oauth-toolkit 
    firebase-admin 
    django-cors-headers
    celery
    django-celery-beat
    django-cors-headers
    django-memcached
    python-memcached
    pymemcache
    channels['daphne']

NOTES:
______
    - For celery to work, you need to set up a broker, for example, RabbitMQ or Redis. see https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html and set it in settings.py
    - Create a celery.py file in your project folder and set up the celery app see https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
    - For django-celery-beat to work, you need to set up a scheduler, for example, RabbitMQ or Redis. see https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#starting-the-scheduler and set it in settings.py
    - For firebase to work, you need to set up a firebase project and download the credentials file and set it in settings.py as FIREBASE_CONFIG = os.path.join(BASE_DIR, 'firebase-credentials.json') see https://firebase.google.com/docs/admin/setup
    - For django-oauth-toolkit to work, you need to set up the authentication backend in settings.py as AUTHENTICATION_BACKENDS = ['oauth2_provider.backends.OAuth2Backend'] see https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-1-configure-your-authentication-backends
    - For django-cors-headers to work, you need to set up the middleware in settings.py as MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', 'django.middleware.common.CommonMiddleware'] see
    

COMMANDS:
_________

check if settings are set correctly
.. code-block:: bash
    
    ./manage.py nets-settings

create settings required for nets_core
.. code-block:: bash
    
    ./manage.py nets-settings --create 

force create settings required for nets_core and overwrite existing settings if any
.. code-block:: bash

    ./manage.py nets-settings --create --force 

create superuser
.. code-block:: bash

    ./manage.py createsuperuser



INSTALLATION
____________

.. code-block:: bash

    pip install django-nets-core

Add 'nets_core' to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'oauth2_provider', # required for authentication
        'nets_core',
    ]

Include the nets_core URLconf in your project urls.py like this:

.. code-block:: python

    path("", include("nets_core.auth_urls", namespace="auth")),


USAGE
_____


.. code-block:: python

    # this already include csrf_exempt for API requests
    from nets_core.decorators import request_handler
    from nets_core.params import RequestParam
    from django.http import JsonResponse

    from .models import MyModel

    @request_handler(
        MyModel, # model that you want to use if view requires it, this return 404 if not found and check ownership or permissions test in can_do param
        index_field='id' # field that will be used to get object from model, default is 'id',

        # params list that you want to get from request
        # this will be validated and converted to python types
        # if something is missing or wrong type, error will be raised
        # if public is True, this will be public in API and auth is not required
        # ensure you set you authentication methods in settings include OAuth2
        params=[
            RequestParam('name', str, optional=False),
        ],
        public=False, # default is False
        # if ProjectMemberModel has role field can_do can be use with role names
        # can_do='role:admin' will check if user has role admin in project or is owner of object
        can_do='myapp.can_delete_object', # this will be check permission to do action, if not passed, only owner of object can do action, if permission does not exists will be created
        perm_required=False, # default is False, this will check if user has permission to do action or is owner of object, if set to TRUE only acces will be granted if can_do is passed

    )
    def my_view(request):
        # do something
        return JsonResponse({'ok': True})
        

Cache is required for verification code:
check https://docs.djangoproject.com/en/4.1/topics/cache/ and pick your preference 
cache engine and set it in settings.py.

.. code-block:: python

    CACHES = {
        'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211'
        }
    }


settings VARS:
______________

And set of lazy API request handlers and commong tasks. Just use it if you are really sure that you dont want to repeat common tasks in request from many sources.
settings VARS:

@request_handle
    include csrf_exempt

Cache is required for verification code:
check https://docs.djangoproject.com/en/4.1/topics/cache/ and pick your preference cache engine.

.. code-block:: python

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }


Sending emails
______________

To send emails with advanced features, use send_email function from nets_core.mail module

.. code-block:: python

    from nets_core.mail import send_email


params:
^^^^^^^

    subject: str, # subject of email
    email: str|list[str], # email or list of emails to send email
    template: str, # template to use for email
    context: dict, # context to use in template
    txt_template: str = None, # text template to use for email, if not set, will use template
    to_queued: bool = True, # if True will be saved to database and sent by celery task, if False will be sent immediately
    force: bool = False, # if True will send email even if NETS_CORE_EMAIL_DEBUG_ENABLED is False
    html: str = None, # html content to use in email, if not set will use template

.. code-block:: python

    from nets_core.mail import send_email

    # example of use
    email_sent, reason, description = send_email(
        subject='Subject of email',
        email=['someone@gmail.com', 'somefake@excludedomain.com'],
        template='myapp/email_template.html',
        context={
            'news_title': 'This is a title',
            'news_content': 'This is a content',
        },
        txt_template='myapp/email_template.txt',
        to_queued=True,
    )

    if not email_sent:
        print(f'Email not sent, reason: {reason}, description: {description}')

    # if NETS_CORE_EMAIL_EXCLUDE_DOMAINS is set, emails to excluded domains will not be sent example: ['excludedomain.com']
    # will sent only to valid emails in email list and description will include excluded emails
    # domain exclude can be set with * to exclude all emails that end with the string before the *
    # example: ['fakeemail*'] will exclude all emails that end with fakeemail: fakeemail.com, fakeemail.org, fakeemail1.com, etc.


Reason returned can be:
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    EMAIL_REASONS = {
        'invalid_email': _('Invalid email address'),
        'email_domain_excluded': _('Email domain is in NETS_CORE_EMAIL_EXCLUDE_DOMAINS'),
        'empty_email': _('Email is empty'),
        'template_not_found': _('Template does not exist'),
        'template_syntax_error': _('Template syntax error'),
        'template_or_html_required': _('template or html content for send_email is required'),
        'email_not_sent': _('Email wasn\'t sent'),
        'email_sent': _('Email sent'),
        'email_in_queue': _('Email in queue.'),
        'email_disabled': _('emails are disabled while debug is true in settings')
    }
    



NETS_CORE SETTINGS
__________________

Enabled multi project support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    NETS_CORE_PROJECT_MODEL = 'myapp.MyProjectModel'
    NETS_CORE_PROJECT_MEMBER_MODEL = 'myapp.MyProjectMemberModel'

Note that both models should be defined in your settings file. Both require def __str__(self): to be defined.
If enabled roles and permissions will be check over project and membership enabled	
example of models:

.. code-block:: python

    from nets_core.models import OwnedModel, NetsCoreBaseModel
    # use of OwnedModel is optional, but recommended to include user, created and updated fields, 
    # if not used, include user, created and updated fields in your model
    class MyProjectModel(OwnedModel):
        name = models.CharField(max_length=255)
        enabled = models.BooleanField(default=True)
        description = models.TextField(blank=True, null=True)

        PROTECTED_FIELDS = ['user']
        JSON_DATA_FIELDS=['name', 'description', 'enabled', 'created', 'updated' ] # OPTIONAL, but recommended is extends OwnedModel or NetsCoreBaseModel , fields to include in json data if to_json is called witout fields parameter

        def __str__(self):
            return self.name

    MEMBER_ROLES = [
        ('superuser', 'Superuser'),
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('viewer', 'Viewer')
    ]
    class MyProjectMemberModel(OwnedModel):
        project = models.ForeignKey(MyProjectModel, on_delete=models.CASCADE)        
        is_superuser = models.BooleanField(default=False)
        enabled = models.BooleanField(default=True)    
        role = models.CharField(max_length=255, choices=MEMBER_ROLES, default='member')  # OPTIONAL but recommended to use in access control by roles see can_do param in request_handler
        JSON_DATA_FIELDS = ['id', 'is_superuser', 'role', 'user'] # User is a ForeignKey to user model, foreign models to include in json data should extend OwnedModel or NetsCoreBaseModel and include JSON_DATA_FIELDS is required

        PROTECTED_FIELDS = ['is_superuser', 'project']
        

        def __str__(self):
            return f'{self.user} - {self.project}'


        # example of custom method to convert member to json
        # each model that extends OwnedModel or NetsCoreBaseModel
        # has a to_json method that can be used to convert the model to json    
        def member_to_json(self):
            """
            Convert the member object to a JSON representation.

            :return: A dictionary representing the member object in JSON format.
            """
            return {
                'id': self.id,
                'project_id': self.project.id,
                'user_id': self.user.id,
                'role': self.role,
                'user': self.user.to_json(fields=('id', 'first_name', 'last_name')),
            }

Setting  is_superuser to True will give user superuser permissions over project, OwnedModel is Abstract model that include user, created and updated fields

.. warning::
   The `NetsCoreBaseModel` is an abstract model that includes `created` and `updated` fields. It implements a `to_json` method that allows the model to be serialized to JSON. This method accepts fields as a tuple to include or `"__all__"` to include all fields. This is a stored function in the database for fast access to JSON data.

   `PROTECTED_FIELDS` is a list of fields that will not be exposed, even if the request includes these fields. If `PROTECTED_FIELDS` is not set, all fields that contain any `NETS_CORE_GLOBAL_PROTECTED_FIELDS` will be removed from the response. For example, fields such as `'old_password'`, `'password'`, `'origin_ip'`, `'ip'` will be removed from the response if not set in `PROTECTED_FIELDS` in your model class. You can set `NETS_CORE_GLOBAL_PROTECTED_FIELDS` in your `settings.py` to replace the default fields to be protected.

   `NetsCoreBaseModel` includes `updated_fields`, which is a `JSONField` that will store changes in the model. This field will be updated by `nets_core` when the model is updated. This is useful for tracking changes in the model. Do not make changes to this field, as it will be updated by `nets_core`.

   `OwnerModel` extends `NetsCoreBaseModel` and includes a `user` field. This is useful for tracking the ownership of the model and will be used to check if a user is the owner of the model.

    TODO: include examples of use to serialize model to json based on fields required per view or endpoint. Inspired in Facebook GraphQL


set NETS_CORE_GLOBAL_PROTECTED_FIELDS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    NETS_CORE_PROTECTED_FIELDS = [
        'password',
        'is_active',
        'enabled',
        'staff',
        'superuser',
        'verified',
        'deleted',
        'token',
        'auth',
        'perms',
        'groups',
        'ip',
        'email',
        'doc',
        'permissions',
        'date_joined',
        'last_login',
        'verified',
        'updated_fields'
    ] # default fields to be protected


Set verification code expire time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    NETS_CORE_VERIFICATION_CODE_EXPIRE_SECONDS = 15*60 # 900 seconds


Set default verification code while DEBUG is True
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, verification code will be 123456 if DEBUG is True, this will avoid sending emails in development and testing
if you want to set a different code, set NETS_CORE_DEBUG_VERIFICATION_CODE

.. code-block:: python

    NETS_CORE_DEBUG_VERIFICATION_CODE = '654321' # default is 123456 if not set

.. warning::

    If NETS_CORE_EMAIL_DEBUG_ENABLED is set to True, emails will be sent in development and testing and code will randomly generated.


Set email footer
^^^^^^^^^^^^^^^^

.. code-block:: python

    NETS_CORE_EMAIL_FOOTER_ENABLED = True 
    NETS_CORE_EMAIL_FOOTER = '<p>Thank you for using our service </p>' # html email footer
    NETS_CORE_EMAIL_FOOTER_TEMPLATE = 'myapp/email_footer.html' # template to use for email footer


.. warning::
    
    If NETS_CORE_EMAIL_FOOTER_TEMPLATE is set, NETS_CORE_EMAIL_FOOTER will be ignored


Set email debug
^^^^^^^^^^^^^^^

Enable sent emails while settings.DEBUG is True, default to False. Enable if you want sent emails in development

.. code-block:: python

    NETS_CORE_EMAIL_DEBUG_ENABLED = True


Set excluded domains
^^^^^^^^^^^^^^^^^^^^

Sometimes you want to exclude some domains from sent emails to avoid spamming, like temporary emails or testing domains
like service providers as mailinator.com, temp-mail.org, guerillamail.com, emailondeck.com, ironmail.com, cloakmail.com, 10minutemail.com, 33mail.com, maildrop.cc, etc.

.. code-block:: python

    NETS_CORE_EMAIL_EXCLUDE_DOMAINS = ['mailinator*', 'temp-mail.org', 'guerillamail.com', 'emailondeck.com', 'ironmail.com', 'cloakmail.com', '10minutemail.com', '33mail.com', 'maildrop.cc']

This will avoid to send emails to these domains: example user request access with me@guerillamail.com will not receive any email
domains can contain * to exclude all emails that end with the string before the * example: ['mailinator*'] will exclude all emails that end with mailinator: mailinator.com, mailinator.org, mailinator1.com, etc.

if a email list is provided to send_email function, emails to excluded domains will not be sent and description will include excluded emails, valid emails will be sent.

.. warning::

    see Sending emails for more info


Set verification code cache key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set cache key to store verification code, default is 'NC_T'
.. code-block:: python

    NETS_CORE_VERIFICATION_CODE_CACHE_KEY = 'NC_T'


Exclude fields from user model to be updated by auth.urls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

nets_core.auth_urls provide endpoints to update user model fields, you can exclude some fields from being updated by auth.urls

Set fields that should not be updated by auth.urls

.. code-block:: python

    PROTECTED_FIELDS = [
        "password",
        "is_superuser",
        "is_staff",
        "is_active",
        "verified",
        "email_verified",
        "last_login",
        "date_joined",
        "updated_fields",
        "groups",
        "user_permissions",
        "doc_*",
    ]
    # set this in your settings.py to exclude fields from user model to be updated by auth.urls
    NETS_CORE_USER_PROHIBITED_FIELDS = prohibited_fields


Include nets_core.auth_urls
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To enabled authentication provided by nets_core include auth.urls in your project urls.py

.. code-block:: python
    
    from django.urls import path, include

    urlpatterns = [
        ...
        path("", include("nets_core.auth_urls", namespace="auth")),
        ...
    ]

This will include the following endpoints:

.. code-block:: python

    urlpatterns = [        
        path('login/', views.auth_login, name='login'),
        path('logout/', views.auth_logout, name='logout'),
        path('authenticate/', views.auth, name='authenticate'),
        path('update/', views.update_user, name='update'),
        path('getProfile/', views.auth_get_profile, name='getProfile'),
        # request account deletion, complain with GDPR see https://gdpr.eu/right-to-be-forgotten/ 
        # and google https://support.google.com/googleplay/android-developer/answer/13327111?hl=en
        # to deploy apps in google play store
        # to expand info to this view include NETS_CORE_DELETE_ACCOUNT_TEMPLATE in settings.py
        path('requestDelete/', views.request_delete_user_account, name='requestDelete'), 
        path('delete/', views.delete_user_account, name='delete'),
    ]

Login Request and Authentication:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. note::
    Requirement:

    Create a new OAuth2 application in your Django admin, this will provide you with a client_id and client_secret.
    see: https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_01.html#create-an-oauth2-client-application

Django-nets-core implement OTP authentication for login, this will send an email with a verification code to the user email,
send POST request to /login/ with USERNAME_FIELD of user model.

.. code-block:: JavaScript

    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: 'myUsername', // if you set the USERNAME_FIELD to email then use email parameter
            // device is optional, if provided will link verification code to device
            // required if you want to use firebase messaging to send push notifications
            // only in login request are accepted device registration, you can implement your own device registration
            // from nets_core.models import UserDevice
            device: {            
                "name": "device name",
                "os": "os",
                "os_version": "os_version",
                "device_token": "device_token",
                "firebase_token": "firebase_token",
                "app_version": "app_version",
                "device_id": "device_id",
                "device_type": "device_type",
            }
        })
    })
    .then(response => response.json()) // {res: 1, data: "CODE SENT", extra: {device_uuid: 'uuid'}}
    ... 

This will send an email with a verification code to the user email, send POST request to /authenticate/ with the verification code
if device is provided, the device_uuid is required to complete the authentication.

.. note::
    If User model has email_verified field, this will be set to True after first successful authentication

.. code-block:: JavaScript

    fetch('/authenticate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: 'myUsername', // should match with USERNAME_FIELD of user model ex: email: 'my@email.com'
            code: '123456', // verification code if DEBUG is True, code will be always 123456 and emails will not be sent, except if NETS_CORE_EMAIL_DEBUG_ENABLED is True
            client_id: 'client_id',
            client_secret: 'client_secret',
            device_uuid: 'uuid' // optional, required if device is provided in login request
        })
    })
    .then(response => response.json()) // {res: 1, data: "AUTHENTICATED", extra: {access_token: 'token', refresh_token: 'refresh_token'}}
    
    // success response
    {
        "access_token": access_token.token,
        "refresh_token": refresh_token.token,
        "token_expire": access_token.expires,
        "user": jsonUser // set JSON_DATA_FIELDS in your user model to include fields in jsonUser or override to_json method
    }
    // error response
    {
        "res": 0,
        "error": "error message"
    }


Authenticated requests:
^^^^^^^^^^^^^^^^^^^^^^^

Include access_token in Authorization header to authenticate requests

.. code-block:: JavaScript

    fetch('/myview/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    })
    .then(response => response.json())


Logout:
^^^^^^^

Send POST request to /logout/ with access_token in Authorization header to logout
cookies will be removed and access_token will be invalidated

.. code-block:: JavaScript

    fetch('/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token,
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json()) // {res: 1, data: "LOGGED OUT"}

Update user model fields:
^^^^^^^^^^^^^^^^^^^^^^^^^

.. WARNING:: 
    PROTECT SENSITIVE FIELDS

    To protect sensitive fields, some fields are prohibited from being updated, see NETS_CORE_USER_PROHIBITED_FIELDS



.. NOTE::
    Only authenticated user

    This endpoint only updated the authenticated user, to update other users use Django admin or your own endpoint

Send POST request to /update/ with access_token in Authorization header to update user model fields

.. code-block:: JavaScript

    fetch('/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token,
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            first_name: 'new first name',
            last_name: 'new last name',
            ... // other fields to update
        })
    })
    .then(response => response.json()) // {res: 1, data: {...jsonUser}}


Get user profile:
^^^^^^^^^^^^^^^^^

.. NOTE:: 
    Only authenticated user
    
    This endpoint only return the authenticated user profile, implement your own endpoint

Send GET request to /getProfile/ with access_token in Authorization header to get user profile

.. code-block:: JavaScript

    fetch('/getProfile/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    })
    .then(response => response.json()) // {res: 1, data: {...jsonUser}}


Request account deletion:
^^^^^^^^^^^^^^^^^^^^^^^^^

Link users to /requestDelete/ to request account deletion, render a form to confirm account deletion


Delete user account:
^^^^^^^^^^^^^^^^^^^^

To implement your own view to confirm account deletion, request an access code to /login/ then 
Send POST request to /delete/ two parameters sure and code.

.. code-block:: JavaScript

    fetch('/delete/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token,
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            sure: true, // required to confirm account deletion
            code: '123456' // verification code to confirm account deletion, should be requested in /requestDelete/
        })
    })
    .then(response => response.json()) // {res: 1, data: "Account deleted successfully"}


To ensure this deletion run without errors, set CASCADE in all relations to user model,
this will delete all related objects to user model, if not set CASCADE, this will raise an error and account will not be deleted.

.. code-block:: python

    class MyModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)

    class MyModel2(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)

Enabled testers for tests or third party verifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enabling testers will allow test autentication without receiving email verification code, for this to work
you need to set the following settings

.. code-block:: python

    NETS_CORE_TESTERS_EMAILS = ['google_testers234*', 'tester1@myappdomain.com']
    NETS_CORE_TESTERS_VERIFICATION_CODE = '475638'


NETS_CORE_TESTERS_EMAILS is a list of emails that will be allowed to authenticate without receiving email verification code
this could end with \* to allow all emails that start with the string before the \*, for production use a strong string and different for each project 
and environment, to avoid unauthorized access

NETS_CORE_TESTERS_VERIFICATION_CODE is the verification code that will be used to authenticate testers

.. warning::

    Use a unique and strong string emails and verification code for each project and environment to avoid unauthorized access


Customize account deletion template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To customize the account deletion email template, create a template in your project templates folder
and set the path in settings.py

.. code-block:: python

    NETS_CORE_DELETE_ACCOUNT_TEMPLATE = 'myapp/account_deletion.html'

This will  include and info template in account deletion view.


.. warning::

    If NETS_CORE_DELETE_ACCOUNT_TEMPLATE is not set not info template will be included in account deletion view




.. code-block:: python

    # login url accept device to link verification code to device
     valid_device_fields = [
        "name",
        "os",
        "os_version",
        "device_token",
        "firebase_token",
        "app_version",
        "device_id",
        "device_type",
    ]

valid_device_fields is use to update or create device
if uuid is provided, device will be updated, otherwise created
if invalid uuid is provided, error will be raised


DJANGO SETTINGS
================

.. code-block:: python

    DEFAULT_FROM_EMAIL is used for emails

    CORS REQUEST AND POST require
    CSRF_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SECURE = True

.. code-block:: python

    # firebase credentials
    # required if you want to use firebase messaging to send push notifications
    FIREBASE_CONFIG = os.path.join(BASE_DIR, 'firebase-credentials.json')
    # "Service account certificates can be downloaded as JSON files from
    # the Firebase console. To instantiate a credential from a certificate file, 
    # either specify the file path or a dict representing the parsed contents of the file."


To generate a firebase credentials file, go to your firebase project configuration,
select service accounts, and generate a new private key, this will download 
a JSON file with your credentials.

Alternatively, you can set FIREBASE_CONFIG environment variable to the path of your
 credentials file.

.. code-block:: bash

    # linux / mac
    export FIREBASE_CONFIG=/path/to/your/firebase-credentials.json
    # windows
    set FIREBASE_CONFIG=/path/to/your/firebase-credentials.json

.. code-block:: python

    # or set it in your settings.py
    FIREBASE_CONFIG = '/path/to/your/firebase-credentials.json'


To send push notifications, you can use the following function:

.. code-block:: python

    from nets_core.firebase_messages import send_user_device_notification
    # to send notification to all devices registered to user
    # will use all tokens registered in nets_core_user_device table
    # returns dict[device.id] = {'success': True, 'message_id': '1234'} or {'success': False, 'error': 'error message'} 
    devices_results = send_user_device_notification(
        user, # user object 
        title: str, # title of notification
        message: str, # body of notification
        data: dict, # data to send with notification, all keys and values should be strings, this will be sent as data in notification
        channel: str = 'default' # channel_id to send notification, default is 'default'
    )
    # to send to a specific device
    from nets_core.firebase_messages import send_fb_message
    send_fb_message(
        title: str, # title of notification
        message: str, # body of notification
        device_token: str, # device token to send notification
        data: dict, # data to send with notification, all keys and values should be strings, this will be sent as data in notification
        channel: str = 'default' # channel_id to send notification, default is 'default'
    )

You can test push notifications with command line:

.. code-block:: bash
    
    # Test with token
    ./manage.py send_push_notification --firebase_token 'device_token' 
    # Test with user id
    ./manage.py send_push_notification --user_id 'user_id'

Additionally, you can set title and message with --title and --message respectively.


Dependencies
============
    Django
    pytz
    python-dateutil
    shortuuid
    django-oauth-toolkit
    firebase-admin
    django-cors-headers



Authentication is made with:
============================
    django-oauth-toolkit
    django-cors-headers



Authentication
==============

    from nets_core.security import authenticate
    authenticate(user, code, client_id, client_secret)

Just to be lazy.
