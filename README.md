# Django Poll Rest
Django's classic Poll quickstart project turned RESTful

If you have followed the [Django Tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) before, you would have created a basic poll application. 

This project shows that basic poll application, but turned RESTful via [Django Rest Framework](https://www.django-rest-framework.org/)

# Pre-requisite of the project

 * Python 3
 * Pipenv
 * docker-compose (optional: to easily run dependencies of the project)
 
# Running The Application

```
cd /path/to/django-poll-rest
docker-compose -f infra/docker-compose.yml up -d 
cd gateway
pipenv shell
python manage.py runserver
```

# Running The Tests

```
cd /path/to/django-poll-rest
cd gateway
pipenv shell
python manage.py test
```

# Appendix

## Some Technical Notes on the Application

 * The site `gateway` and the app `polls` have their own routers defined. But I aggregated all routes inside the site `gateway` into one so that you can see them all in `localhost:8000`
 * I placed `/users/` and `/groups/` routers inside `django-poll-rest/gateway/gateway/urls.py`
 * The app `polls` contains the `/choices/` and `/questsions`/ routes
 * The defualt permission class is my own custom class which is `_common.rest_framework.ext.AccurateDjangoModelPermissions`. This is a subclass of `DjangoModelPermissions`. `DjangoModelPermissions` uses the same permission scheme as that of the admin screen - with the exception of view. For `DjangoModelPermissions`, any logged in user can view the model. So I subclassed it so that only those with `'%(app_label)s.view_%(model_name)s'` can view the permission of the model (_which is similar to how the admin permission scheme does it_).
 * The `/choices/`, and `/questions/` routes uses `rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly` because from the original django tutorial, anybody can see the questions and the choices. Furthermore, voting (i.e. `POST:/questions/{question id}/vote/`) uses permission class `rest_framework.permissions.AllowAny` (_becaus in the original django tutorial, anyone can vote_)
