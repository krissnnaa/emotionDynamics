import json
import requests
import re
import nltk
from gensim.models import Word2Vec
import schedule
import time
login_number = 0
commentCollection = []

def commentsCollection():
    global login_number
    global commentCollection
    output_list = []
    params = {'state': 'all'}
    urlSearch = []
    owner_name='ipython'
    repo_name = 'ipython'

    with open("authentication.json") as outfile:
        authentication = json.load(outfile)
    dest_path = "/home/krishna/PycharmProjects/CommitCollection/commitFolder/"
    url1 = "https://api.github.com/repos/" + owner_name + "/" + repo_name + "/issues"
    url2 = "https://api.github.com/repos/" + owner_name + "/" + repo_name + "/pulls"
    urlSearch.append(url1)
    urlSearch.append(url2)

    for urlin in urlSearch:
        i = 0
        while True:
            print(i)
            url_a = urlin + '?page={0}'.format(i)
            r = requests.get(url_a, params,
                             auth=(authentication[login_number]['username'], authentication[login_number]['password']))

            if not r.json():
                break
            else:
                if r.status_code == 200:
                    print("Yeah successful")
                    issueRequest = r.json()
                    for item in range(len(issueRequest)):
                        if urlin==url2:
                            pull=issueRequest[item]['review_comments_url']
                            req = requests.get(pull, params,
                                               auth=(authentication[login_number]['username'],
                                                     authentication[login_number]['password']))
                            if req.status_code==403:
                                if login_number < 18:
                                    login_number = login_number + 1
                                else:
                                    login_number = 0
                                req = requests.get(pull, params,
                                                   auth=(authentication[login_number]['username'],
                                                         authentication[login_number]['password']))
                                output_list.append(req)
                                continue
                            output_list.append(req)

                        else:
                            issue=issueRequest[item]['comments_url']
                            req = requests.get(issue, params,
                                     auth=(authentication[login_number]['username'],
                                           authentication[login_number]['password']))

                            if req.status_code==403:
                                if login_number < 18:
                                    login_number = login_number + 1
                                else:
                                    login_number = 0
                                req = requests.get(issue, params,
                                                   auth=(authentication[login_number]['username'],
                                                         authentication[login_number]['password']))
                                output_list.append(req)
                                continue
                            output_list.append(req)
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
                                print("Yeah successful")
                                issueRequest = r.json()
                                for item in range(len(issueRequest)):
                                    if urlin == url2:
                                        pull = issueRequest[item]['review_comments_url']
                                        req = requests.get(pull, params,
                                                           auth=(authentication[login_number]['username'],
                                                                 authentication[login_number]['password']))
                                        if req.status_code == 403:
                                            if login_number < 18:
                                                login_number = login_number + 1
                                            else:
                                                login_number = 0
                                            req = requests.get(pull, params,
                                                               auth=(authentication[login_number]['username'],
                                                                     authentication[login_number]['password']))
                                            output_list.append(req)
                                            continue
                                        output_list.append(req)

                                    else:
                                        issue = issueRequest[item]['comments_url']
                                        req = requests.get(issue, params,
                                                           auth=(authentication[login_number]['username'],
                                                                 authentication[login_number]['password']))

                                        if req.status_code == 403:
                                            if login_number < 18:
                                                login_number = login_number + 1
                                            else:
                                                login_number = 0
                                            req = requests.get(issue, params,
                                                               auth=(authentication[login_number]['username'],
                                                                     authentication[login_number]['password']))
                                            output_list.append(req)
                                            continue
                                        output_list.append(req)

                                i += 1
                                break
                    else:
                        break

    output_list=[item for item in output_list if item is not None]
    output_list=list(set(output_list))
    with open(dest_path+'backup.txt','w',encoding='utf-8') as fd:
        for item in output_list:
            fd.write('%s\n'%item)

    memberComment = {}
    for item in output_list:
        for insideItem in item:
            for index in range(len(insideItem)):
                authorAssociation = insideItem[index]['author_association']
                memberName = insideItem[index]['user']['login']
                commentBody = insideItem[index]['body'] + ' '
                createdDate = insideItem[index]['created_at']
                flag = 0

                initialComment = []
                if authorAssociation == 'MEMBER' and createdDate[0]>=2018:
                    for key, value in memberComment.items():
                        if key == memberName:
                            previousComment = memberComment[memberName]
                            commentTuple = (createdDate, commentBody)
                            previousComment.append(commentTuple)
                            memberComment[key] = previousComment
                            flag = 1
                            break

                    if flag == 0:
                        commentTuple = (createdDate, commentBody)
                        initialComment.append(commentTuple)
                        memberComment[memberName] = initialComment

    for key, value in memberComment.items():
        fileRead = open(dest_path + key + "_data.txt", 'w', encoding="utf-8")
        fileRead.write('Created Date\t\t\t\tComments\n')
        value = list(set(value))
        for eachTuple in value:
            preProcess = re.sub(r'[^\w\s]', '', eachTuple[1])
            preProcess = (re.sub(r'[\r\n]+', '', preProcess)).lower()
            fileRead.write('%s\t\t\t%s\n' % (eachTuple[0], preProcess))


if __name__ == '__main__':

    commentsCollection()
    #     tokenWords = nltk.tokenize.word_tokenize(valueString)
    #     preProcessComments[key] = tokenWords
    #     model = Word2Vec([tokenWords], window=6, size=310, negative=5, min_count=1)
    #     model.wv.save_word2vec_format(dest_path + key + '.txt', binary=False)

