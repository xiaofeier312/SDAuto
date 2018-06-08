from app.models import APIProjects, APIModules, APIDoc, APICases, TomcatEnv
import re
import requests
import json
import difflib
import copy
import time
from app.models import db


class SDProjectData(object):
    def get_all_projects(self):
        """return a list, like ['个人中心', '企业家']"""
        all_project = APIProjects.query.all()
        print(all_project)
        return all_project

    def get_all_modules(self):
        all_modules = APIModules.query.all()
        return all_modules

    def get_all_doc(self):
        all_doc = APIDoc.query.all()
        return all_doc

    def get_all_cases(self):
        all_cases = APICases.query.all()
        return all_cases

    def get_module_by_id(self, project_id):
        """past project_name, and get it's modules"""
        if project_id:
            module = APIModules.query.filter_by(id=project_id).first()
        else:
            module = []
        return module

    def get_doc_by_mod_id(self, module_id):
        doc = APIDoc.query.filter_by(id=module_id).all()
        return doc

    def get_case_by_doc_id(self, doc_id):
        case = APICases.query.filter_by(id=doc_id).all()
        return case

    def get_case_obj_by_case_id(self, case_id):
        case_obj = APICases.query.filter_by(id=case_id).first()
        return case_obj

    def optimize_url(self, url):
        ''' if url start with http/ return is https or http with 1 or 0'''
        match_str = '^https://'
        match_str2 = '^http://'
        form_url = url
        if re.findall(match_str, url):
            get_is_https = 1
        elif re.findall(match_str2, url):
            get_is_https = 0
        else:
            form_url = 'http://' + form_url  # if no http:// string, add it
            get_is_https = 0
        return form_url

    def transfer_body_to_dict(self, case_obj):
        """ Transfer str>"data={'a':1}" to dict {"data":"{'a':1}}
        //return a dict"""
        str_body = case_obj.body
        divsion_semi = str_body.split(';')
        dict_body = {}
        for i in divsion_semi:
            first_key = i.split('=', 1)[0]
            second_value = i.split('=', 1)[1]
            dict_body[first_key] = second_value
        return dict_body

    def run_case_id(self, case_id, env_id):
        """run case by single, case_id"""
        db.session.remove()
        case = APICases.query.filter_by(id=case_id).first()
        env = TomcatEnv.query.filter_by(id=env_id).first()
        final_url = self.optimize_url(env.ip + ':' + str(env.port) + '/' + case.url)
        body_dict = self.transfer_body_to_dict(case)
        # final_headers ->> Should be dict, but it is str in mysql database.
        try:
            final_body = json.dumps(case.body)
        except Exception:
            print("@@Error occur: {} ".format(Exception))
            return json.dumps({'result': 'error occur! error number: 11', 'resultCode': 0})

        print('------case.http_method is {}-{}-{}'.format(case.http_method, final_url, case.headers))
        if case.http_method == 'get':
            # 1 is get
            result = requests.request('get', final_url, data=body_dict)
        elif case.http_method == 'post':
            # 2 is post
            print('--post func')
            result = requests.request('post', final_url, params=body_dict)
            print('--case.body:{}=='.format(case.body))
        else:
            result = json.dumps({'result': 'error occur! error number: 12', 'resultCode': 0})
            return result
        return result

    def run_case_tool(self, case_id, old_env, new_env):
        """run case//return result list"""
        print('Run case----')
        old_env_result = self.run_case_id(case_id, old_env)
        new_env_result = self.run_case_id(case_id, new_env)
        old_result2 = self.split_text(old_env_result.text)
        new_result2 = self.split_text(new_env_result.text)
        case_name = self.get_case_obj_by_case_id(case_id).name
        case_body = self.get_case_obj_by_case_id(case_id).body
        # Add case id, name to compare results page
        old_result2.insert(0, 'Case_id_' + str(case_id) + '_name_' + case_name)
        new_result2.insert(0, 'Case_id_' + str(case_id) + '_name_' +  case_name)
        # Add case parameter
        old_result2.insert(1, 'Case_parameter_' + case_body)
        new_result2.insert(1, 'Case_parameter_' + case_body)
        return {'old': old_result2, 'new': new_result2}

    def split_text(self, origin_text):
        """Input origin should be str or list only.
            //use X.splitlines to transfer to list wherher it is str or list
            //splitlines should be deal with list, so we transfer str to list
            //Also try to transfer json to json format to displayed humanityß
            //return list"""
        init_text = []
        if isinstance(origin_text, str):
            init_text.append(origin_text)
        elif isinstance(origin_text, list):
            init_text = copy.deepcopy(origin_text)
        else:
            raise TypeError('only support str and list')
        dealed_text = []
        for i in init_text:
            try:
                s_temp = json.loads(i)
                s_temp2 = json.dumps(s_temp, indent=4, ensure_ascii=False)
                s_temp3 = s_temp2.splitlines()
                for j in s_temp3:
                    dealed_text.append(j)
                continue
            except Exception as e:
                print('@@@Cannt loads: {}'.format(i))
                s_temp4 = i
            dealed_text.append(s_temp4)
        return dealed_text

    # def format_json_for_differ(self, text):
    #     """format json to display json with spaces, return a list"""
    #     init_text = []
    #     init_text.append(text)  # deal with text whether it is a list or a string
    #     result_list = []
    #     init_text = self.split_text(init_text)
    #     for i in init_text:
    #         init_temp = i.splitlines()
    #         init_text += init_temp
    #
    #     for j in init_text:
    #         """try to format json text for look easy"""
    #         try:
    #             s_temp = json.loads(str(i))
    #             s_temp2 = json.dumps(s_temp, indent=4, ensure_ascii=False)
    #         except Exception as e:
    #             print('@@@Cannt loads: {}'.format(i))
    #             s134 = j

    def get_new_file_name(self, case_id, old_env, new_env):
        """return a new case name"""
        date_str = time.strftime("%m-%d-%H:%M:%S")
        file_name = date_str + '_case_' + str(case_id) + '_Compare_env_' + str(old_env) + '-' + str(new_env) + '.html'
        return file_name

    def compare_result(self, case_id, old_env, new_env):
        """compare results and make file"""
        file_name = self.get_new_file_name(case_id, old_env, new_env)

        d = difflib.HtmlDiff()
        f = open('./workResults/' + file_name, 'w')

        results_list = self.run_case_tool(case_id, old_env, new_env)
        print('>>results_list: {}'.format(results_list))
        f.writelines(d.make_file(results_list['old'], results_list['new']))
        f.close()

        return file_name
