import json
import requests
import re
import nltk
from gensim.models import Word2Vec

login_number = 0
commentCollection = []

def load_issues(url=None, owner_name=None, repo_name=None, dest_path=None, authentication=None):
    i = 0
    global login_number
    global commentCollection
    output_list = []
    params = {'state': 'all'}
    while True:
        print(i)
        if url is None:
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
                output_list.append(issueRequest)
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
                            issueRequest = r.json()
                            output_list.append(issueRequest)
                            i += 1
                            break
                else:
                    break

    commentCollection.append(output_list)
    if repo_name is not None:
        with open(dest_path + "/" + repo_name + ".json", "w") as infile:
            json.dump(output_list, infile)

if __name__ == '__main__':
    with open("authentication.json") as outfile:
        authentication = json.load(outfile)
    dest_path = "C:/Users/CoCo Lab/PycharmProjects/commentCollection/pullComments/"
    readingPull = 0
    if readingPull == 1:
        project_ = {'ipython': 'ipython'}
        for key, value in project_.items():
            load_issues(None, key, value, dest_path, authentication)
        with open(dest_path + "ipython.json") as f:
            file = json.load(f)
        commentLinks = []
        issueLinks = []

        for itemList in file:
            for index in range(len(itemList)):
                createdDate = re.findall(r'^\d+', itemList[index]['created_at'])
                if int(createdDate[0]) < 2018:
                    continue
                else:
                    commentLinks.append(itemList[index]['_links']['review_comments']['href'])
                    issueLinks.append(itemList[index]['_links']['comments']['href'])
        commentLinks=list(set(commentLinks))
        issueLinks=list(set(issueLinks))
        with open(dest_path + "commentsFrom2018.txt", 'w') as f:
            f.write(str(commentLinks))
        with open(dest_path + "issueCommentsFrom2018.txt", 'w') as f:
            f.write(str(issueLinks))

        commentCollection=[]
        for item in commentLinks:
            load_issues(item, None, None, dest_path, authentication)
        with open(dest_path + "/" + "commentsCollection" + ".json", "w") as f:
            json.dump(commentCollection, f)
        commentCollection = []
        for item in issueLinks:
            load_issues(item, None, None, dest_path, authentication)
        with open(dest_path + "/" + "issueCommentsCollection" + ".json", "w") as f:
            json.dump(commentCollection, f)

    with open(dest_path + "commentsCollection.json") as f:
        file = json.load(f)
    file = [x for x in file if len(x) > 0]
    with open(dest_path + "issueCommentsCollection.json") as f:
        fileIssue = json.load(f)

    fileIssue = [x for x in fileIssue if len(x) > 0]
    bothFile = [file, fileIssue]
    memberComment = {}
    for item in bothFile:
        for itemList in item:
            for insideItem in itemList:
                for index in range(len(insideItem)):
                    authorAssociation = insideItem[index]['author_association']
                    memberName = insideItem[index]['user']['login']
                    commentBody = insideItem[index]['body'] + ' '
                    createdDate = insideItem[index]['created_at']
                    flag = 0

                    initialComment = []
                    if authorAssociation == 'MEMBER':
                        for key, value in memberComment.items():
                            if key == memberName:
                                previousComment = memberComment[memberName]
                                commentTuple = (createdDate, commentBody)
                                previousComment.append(commentTuple)
                                memberComment[key] =previousComment
                                flag = 1
                                break

                        if flag == 0:
                            commentTuple = (createdDate, commentBody)
                            initialComment.append(commentTuple)
                            memberComment[memberName] = initialComment



    for key,value in memberComment.items():
        fileRead=open(dest_path +key +"_data.txt", 'w', encoding="utf-8")
        fileRead.write('Created Date\t\t\t\tComments\n')
        value=list(set(value))
        for eachTuple in value:
            preProcess=re.sub(r'[^\w\s]', '', eachTuple[1])
            preProcess=(re.sub(r'[\r\n]+','',preProcess)).lower()
            fileRead.write('%s\t\t\t%s\n'%(eachTuple[0],preProcess))

    #     tokenWords = nltk.tokenize.word_tokenize(valueString)
    #     preProcessComments[key] = tokenWords
    #     model = Word2Vec([tokenWords], window=6, size=310, negative=5, min_count=1)
    #     model.wv.save_word2vec_format(dest_path + key + '.txt', binary=False)
