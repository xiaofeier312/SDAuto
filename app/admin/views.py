from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin import expose, BaseView, AdminIndexView
from flask import redirect
from config import NormalConfig

class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    page_size = 10
    column_display_pk = True
    form_excluded_columns = ['create_time', 'op_time','modules']  # remove fields from the create and edit forms

class projectsModelView(ModelView):
    """custom view for projects"""
    column_display_pk = True
    can_view_details = True
    page_size = 10
    column_exclude_list = ['operator', ]
    # column_editable_list = ['name', 'remark']
    column_searchable_list = ['name']
    column_filters = ['name']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time','modules']  # remove fields from the create and edit forms
    # column_select_related_list = ('id','name')


class newItemAjaxModelLoader(QueryAjaxModelLoader):
    def get_list(self, term, offset=0, limit=10):
        query = self.session.query(self.model).filter_by(mid=term)
        return query.offset(offset).limit(limit).all()


class modulesModelView(ModelView):
    """custom view for modules"""
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('name', 'project', 'remark')
    column_list = ('id','name', 'project', 'remark', 'op_time')
    column_default_sort = 'id'
    # column_searchable_list = ('projectID',APIProjects.id)
    # form_ajax_refs = {
    #     # 'projectID': QueryAjaxModelLoader('projectID', db.session, APIProjects, fields=['id', 'name'])
    #     'project': {
    #         'fields': [APIProjects.name],
    #         'page_size': 10
    #     }
    # }



class DocModelView(ModelView):
    """Custom APIDoc view"""
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('name', 'module', 'Api_priority', 'path', 'http_method', 'headers', 'body', 'remark', 'operator')
    column_list = ('id','name', 'module','path', 'remark', 'op_time')
    column_default_sort = 'id'
    # form_ajax_refs = {
    #     'module': {
    #         'fields': [APIModules.name],
    #         'pagesize': 10
    #     }
    # }
    form_choices = {
        'Api_priority':[('1','1'),('2','2'),('3','3')],
        'http_method':[('get','get'),('post','post'),('put','put')]
    }


class caseModelView(ModelView):
    """Custom API cases view"""
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time','Api_priority', 'is_https', 'http_response' ]
    form_columns = ('name', 'doc', 'url', 'headers', 'body', 'remark', 'operator', 'http_method')
    form_choices = {
        'Api_priority':[('1','1'),('2','2'),('3','3')],
        'http_method':[('get','get'),('post','post'),('put','put')]
    }
    column_exclude_list = ['Api_priority', 'is_https', 'http_method', 'http_response']
    column_list = ('id','name', 'doc','url','http_method','body','remark', 'op_time')
    column_default_sort = 'id'


class verifyModelView(ModelView):
    """Custom caseVerify view"""
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('case','verify_path','verify_expect','verify_method','set_up','set_down','operator')


class resultModelView(ModelView):
    """Custom result view"""
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    form_columns = ('task_id','case','result')

class runCaseModelView(ModelView):
    """Custom runCaseModelView"""
    current_server = NormalConfig().get_current_ip()
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['create_time', 'op_time']
    column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-play', current_server+'main/compare_run/{row_id}'),
        # EndpointLinkRowAction('glyphicon glyphicon-film', 'apimodules.index_view')
    ]
    column_list = ('id','name', 'case_id', 'old_','new_','replace','paramter_list','remark', 'op_time')
    column_default_sort = 'id'


class ReviewResultModelView(BaseView):
    @expose('/')
    def check_result(self):
        return self.render('/admin/contain_ftp_page.html')



class myAdminModelView(AdminIndexView):
    @expose('/')
    def index(self):
        return redirect('/admin/runcase/')

class BlueprintTaskModelView(ModelView):
    current_server = NormalConfig().get_current_ip()
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['operator']
    column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-play', current_server+'task/divide_task/{row_id}'),
        # EndpointLinkRowAction('glyphicon glyphicon-film', 'apimodules.index_view')
    ]

class BlueprintSubTaskModelView(ModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['operator']