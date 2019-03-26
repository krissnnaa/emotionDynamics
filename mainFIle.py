import json
import requests

login_number = 0


def load_issues( owner_name, repo_name, dest_path, authentication):
    i = 0
    global login_number
    with open(dest_path + "/" + repo_name + ".json", "w") as infile:
        params = {'state': 'all'}
        while True:
            print(i)
            url = "https://api.github.com/repos/" + owner_name + "/" + repo_name + "/pulls"
            url_a = url + '?page={0}'.format(i)
            r = requests.get(url_a, params,
                             auth=(authentication[login_number]['username'], authentication[login_number]['password']))

            if not r.json():
                break
            else:
                if r.status_code == 200:
                    print("Yeah successful")
                    issueRequest = r.json()
                    json.dump(issueRequest, infile)
                    i += 1
                else:
                    error = r.json()
                    print(repo_name + '\t has an error message:\n' + error['message'])
                    if r.status_code == 403:
                        print(r.status_code)
                        if login_number < 18:
                            login_number = login_number + 1
                        else:
                            login_number = 0
                        while True:
                            r = requests.get(url_a, auth=(
                            authentication[login_number]['username'], authentication[login_number]['password']))
                            if r.status_code == 200:
                                print("Yeah Successful")
                                pullrequest = r.json()
                                json.dump(pullrequest, infile)
                                i += 1
                                break
                    else:
                        break


if __name__=='__main__':

    with open("authentication.json") as outfile:
        authentication = json.load(outfile)

    dest_path = "/home/krishna/PycharmProjects/CommitCollection/pullFolder/"
    project_={'ipython':'ipython','apache':'incubator-echarts'}

    for key,value in project_.items():
        load_issues(key, value, dest_path, authentication)

