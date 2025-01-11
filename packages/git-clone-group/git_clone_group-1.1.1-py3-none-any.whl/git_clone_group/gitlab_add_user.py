import json
import os
import shlex
import subprocess
import time
import requests
from urllib.request import urlopen


def get_next(group_id, page=None):
    if page is None:
        page = 1
    url = gen_next_url(group_id, page)
    all_projects = urlopen(url)
    all_projects_dict = json.loads(all_projects.read().decode())
    if len(all_projects_dict) == 0:
        return
    for thisProject in all_projects_dict:
        try:
            this_project_url = thisProject['ssh_url_to_repo']
            this_project_path = thisProject['path_with_namespace']
            print('donwload project', this_project_url + ' ' + this_project_path)
            full_path = dest_dir + this_project_path
            if os.path.exists(full_path):
                command = shlex.split('git -C "%s" pull' % (full_path))
            else:
                this_project_path = dest_dir + this_project_path
                command = shlex.split('git clone %s %s' % (this_project_url, this_project_path))
            result = subprocess.run(command)
            print(command, " commadn exec is ", result.returncode)
        except Exception as e:
            print("Error on ", e)
    page = page + 1
    get_next(group_id, page)


def have_next_projects(group_id):
    url = gen_next_url(group_id)
    all_projects = urlopen(url)
    all_projects_dict = json.loads(all_projects.read().decode())
    all_projects.close()  # Close the response to avoid memory leak
    if len(all_projects_dict) == 0:
        return False
    return True


def get_sub_groups(parent_id):
    url = gen_subgroups_url(parent_id)
    all_projects = urlopen(url)
    all_projects_dict = json.loads(all_projects.read().decode())
    sub_ids = []
    if len(all_projects_dict) == 0:
        return sub_ids
    for thisProject in all_projects_dict:
        try:
            id = thisProject['id']
            sub_ids.append(id)
        except Exception as e:
            print("Error on ", e)
    return sub_ids


def cal_next_sub_group_ids(parent_id):
    parent = ''
    parent = parent_id
    is_start = 1
    parent_list = set()
    sub_ids = get_sub_groups(parent_id)
    ok = have_next_projects(parent_id)
    if len(sub_ids) != 0 and ok is False:
        for i in range(len(sub_ids)):
            print(sub_ids[i])
            parent = sub_ids[i]
            a = cal_next_sub_group_ids(sub_ids[i])
            return a
    if len(sub_ids) != 0 and ok is True:
        for i in range(len(sub_ids)):
            parent = sub_ids[i]
            parent_list.add(sub_ids[i])
            a = cal_next_sub_group_ids(sub_ids[i])
            parent_list.union(a)
    if len(sub_ids) == 0 and ok is True:
        parent_list.add(parent)
        return parent_list
    if len(sub_ids) == 0 and ok is False:
        return parent_list
    return parent_list


def download_code(parent_id):
    data = cal_next_sub_group_ids(parent_id)
    if have_next_projects(parent_id):
        data.add(parent_id)
    for group_id in data:
        get_next(group_id)
    return


def gen_next_url(target_id, page=None):
    if page is None:
        page = 1
    return "http://%s/api/v4/groups/%s/projects?page=%s&private_token=%s" % (gitlabAddr, target_id, page, gitlabToken)


def gen_subgroups_url(target_id):
    return "http://%s/api/v4/groups/%s/subgroups?private_token=%s" % (gitlabAddr, target_id, gitlabToken)


def gen_global_url():
    return "http://%s/api/v4/projects?private_token=%s" % (gitlabAddr, gitlabToken)

def add_user_to_group(group_id, user_id):
    headers = {'Private-Token': gitlabToken}
    data = {'user_id': user_id, 'access_level': 50}
    response = requests.post(f'http://{gitlabAddr}/api/v4/groups/{group_id}/members', headers=headers, data=data)
    if response.status_code == 201:
        print(group_id, "User added successfully")
    else:
        print("Failed to add user", response.json())

def update_user_level(group_id, user_id, level):
    headers = {'Private-Token': gitlabToken}
    data = {'user_id': user_id, 'access_level': level}
    response = requests.put(f'http://{gitlabAddr}/api/v4/groups/{group_id}/members/{user_id}', headers=headers, data=data)
    if response.status_code == 200:
        print(group_id, "User updated successfully")
    else:
        print("Failed to update user", response.json())


def gen_group_url(page, per_page):
    return "http://%s/api/v4/groups?private_token=%s&page=%s&per_page=%s" % (gitlabAddr, gitlabToken, page, per_page)


def download_global_code():
    url = gen_global_url()
    all_projects = urlopen(url)
    all_projects_dict = json.loads(all_projects.read().decode())
    if len(all_projects_dict) == 0:
        return
    for thisProject in all_projects_dict:
        try:
            this_project_url = thisProject['ssh_url_to_repo']
            this_project_path = thisProject['path_with_namespace']
            print('donwload project', this_project_url + ' ' + this_project_path)

            if os.path.exists(this_project_path):
                command = shlex.split('git -C "%s" pull' % (this_project_path))
            else:
                command = shlex.split('git clone %s %s' % (this_project_url, this_project_path))
            result = subprocess.run(command)
            print(command, " commadn exec is ", result.returncode)
            time.sleep(1)
        except Exception as e:
            print("Error on ", e)
    return


def main(group_name):
    if group_name == '':
        download_global_code()
    else:
        url = gen_group_url()
        all_projects = urlopen(url)
        all_projects_dict = json.loads(all_projects.read().decode())
        if len(all_projects_dict) == 0:
            return
        target_id = ''
        for thisProject in all_projects_dict:
            try:
                this_name = thisProject['name']
                if group_name == this_name:
                    target_id = thisProject['id']
                    break
            except Exception as e:
                print("Error on", e)
        download_code(target_id)
        return

def add_ssh_key_to_user(user_id, title, key):
    headers = {'Private-Token': gitlabToken}
    data = {'title': title, 'key': key}
    response = requests.post(f'http://{gitlabAddr}/api/v4/users/{user_id}/keys', headers=headers, data=data)
    if response.status_code == 201:
        print(user_id, "Key added successfully")
    else:
        print("Failed to add key", response.json())

def add_user_to_gitlab(username, email, password):
    headers = {'Private-Token': gitlabToken}
    data = {'email': email, 'password': password, 'username': username, 'name': username}
    response = requests.post(f'http://{gitlabAddr}/api/v4/users', headers=headers, data=data)
    if response.status_code == 201:
        print("User added successfully")
    else:
        print("Failed to add user", response)

if __name__ == '__main__':
    gitlabToken = 'glpat-AnnNTyW8zEsAiTz4uJDY'
    # gitlabToken = 'awo1Tmxap9Ra6W_Fv-TG'
    gitlabAddr = '47.95.217.115'
    target = 'hualalapay'
    # add_user_to_gitlab
    add_user_to_gitlab('bpzhang1','zhangbingpeng@hualala.com','12@wed#')
