from flask_admin.contrib.sqla import ModelView
from app.models import APIProjects
from .services import DataChoice
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from app import db

###
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import APIProjects, APIModules
###

class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    page_size = 10


class projectsModelView(ModelView):
    """custom view for projects"""
    can_view_details = True
    page_size = 10
    column_exclude_list = ['operator', ]
    # column_editable_list = ['name', 'remark']
    column_searchable_list = ['name']
    column_filters = ['name']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']  # remove fields from the create and edit forms


class modulesModelView(ModelView):
    """custom view for modules"""
    can_view_details = True
    page_size = 10
    # column_exclude_list = ['operator', ]
    # column_editable_list = ['name', 'remark']
    column_searchable_list = ['name']
    column_filters = ['name']
    create_modal = True
    edit_modal = True

    # pros = APIProjects.query.all() # Will 'Either work inside a view function or push an application context'
    # form_choices = {
    #     'projectID': DataChoice.get_projects()
    # }

    # engine = create_engine('mysql+pymysql://alimysql:alimysql7933@47.98.133.163/sdauto?charset=utf8', echo=True)
    # DBsession = sessionmaker(bind=engine)
    # session = DBsession()
    # from_ajax_refs = {
    #     'projectID':{'fields':APIProjects.name}
    # }
    # form_ajax_refs = {
    #     'projectID':QueryAjaxModelLoader('name',session,APIProjects,filters=['id>0'],fields=['name'])
    # }
    # DataChoice.clear_db_session()
    form_excluded_columns = ['create_time', 'op_time']